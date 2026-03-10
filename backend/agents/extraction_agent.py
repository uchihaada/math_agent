import io
import re
import tempfile
from pathlib import Path

import cv2
import numpy as np
from langchain_core.messages import HumanMessage, SystemMessage
from PIL import Image
from pydantic import BaseModel, Field

from backend.llm.llm import get_llm
from backend.memory.memory_store import apply_learned_corrections
from backend.models.schemas import ExtractionResponse
from backend.utils.llm_json import invoke_json_model

_ocr_reader = None
_whisper_model = None
_ocr_repair_llm = None
MAX_OCR_ALTERNATIVES = 3
MATH_ALLOWLIST = (
    "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "+-=*/()[]{}<>.,:^_|% "
)
NOISY_OCR_PATTERNS = ("_", " i+0", " l+0", " 1+0", "ez", "e z")


class OCRRepairOutput(BaseModel):
    text: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)


def _get_ocr_reader():
    global _ocr_reader

    if _ocr_reader is None:
        import easyocr

        _ocr_reader = easyocr.Reader(["en"], gpu=False)

    return _ocr_reader


def _get_whisper_model():
    global _whisper_model

    if _whisper_model is None:
        import whisper

        _whisper_model = whisper.load_model("base")

    return _whisper_model


def _get_ocr_repair_llm():
    global _ocr_repair_llm

    if _ocr_repair_llm is None:
        _ocr_repair_llm = get_llm()

    return _ocr_repair_llm


def _normalize_math_phrases(text: str):
    replacements = [
        (r"\bsquare root of\b", "sqrt "),
        (r"\braised to\b", "^"),
        (r"\bto the power of\b", "^"),
        (r"\bdivided by\b", "/"),
        (r"\bmultiplied by\b", "*"),
        (r"\bplus\b", "+"),
        (r"\bminus\b", "-"),
        (r"\bopen bracket\b", "("),
        (r"\bclose bracket\b", ")"),
        (r"\bx squared\b", "x^2"),
        (r"\bx cubed\b", "x^3"),
        (r"\by squared\b", "y^2"),
        (r"\by cubed\b", "y^3"),
    ]

    normalized = text
    for pattern, replacement in replacements:
        normalized = re.sub(pattern, replacement, normalized, flags=re.IGNORECASE)

    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _normalize_math_ocr_text(text: str):
    normalized = text.replace("\n", " ")
    replacements = [
        ("\u00e2\u20ac\u201d", "-"),
        ("\u2212", "-"),
        ("\u00c3\u00b7", "/"),
        ("\u00c3\u2014", "*"),
        ("\u00e2\u02c6\u2022", "/"),
        ("\u00e2\u0081\u201e", "/"),
        ("\u00c2\u00a6", "|"),
        ("\u00c2\u00a2", "c"),
        ("_", "-"),
    ]

    for source, target in replacements:
        normalized = normalized.replace(source, target)

    normalized = re.sub(r"\b[l1i|]im\b", "lim", normalized, flags=re.IGNORECASE)
    normalized = re.sub(
        r"\blim\s*[l1i|xyzt]\s*\+\s*0(?=\b|[xyz(])",
        "lim x->0 ",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(
        r"\blim\s*[xxyz]?\s*[-=~>]+\s*0(?=\b|[xyz(])",
        "lim x->0 ",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(r"\blim\s*x\s*->\s*0\b", "lim x->0", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\be\s*z\b", "e^x", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\be\s*([xy])\b", r"e^\1", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\bez\b", "e^x", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\b([xyz])\s*([23456789])\b", r"\1^\2", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\b(sin|cos|tan|log|ln)([xyz])\b", r"\1 \2", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"\s*\+\s*", " + ", normalized)
    normalized = re.sub(r"\s*-\s*", " - ", normalized)
    normalized = re.sub(r"\s*/\s*", " / ", normalized)
    normalized = re.sub(r"\s*\^\s*", "^", normalized)
    normalized = re.sub(r"-\s*>", "->", normalized)
    normalized = re.sub(r"\s+->\s*", "->", normalized)
    normalized = re.sub(r"->\s+", "->", normalized)
    normalized = re.sub(r"\(\s+", "(", normalized)
    normalized = re.sub(r"\s+\)", ")", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def _apply_runtime_corrections(text: str):
    normalized_text = _normalize_math_phrases(text)
    normalized_text = _normalize_math_ocr_text(normalized_text)
    corrected_text, applied_corrections = apply_learned_corrections(normalized_text)
    return corrected_text, applied_corrections


def _crop_foreground(gray_image: np.ndarray):
    working = gray_image
    if float(gray_image.mean()) < 140:
        working = 255 - gray_image

    blurred = cv2.GaussianBlur(working, (5, 5), 0)
    _, mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    coords = cv2.findNonZero(mask)
    if coords is None:
        return gray_image

    x, y, width, height = cv2.boundingRect(coords)
    if width < gray_image.shape[1] * 0.15 or height < gray_image.shape[0] * 0.10:
        return gray_image

    padding = max(12, int(max(width, height) * 0.03))
    x0 = max(0, x - padding)
    y0 = max(0, y - padding)
    x1 = min(gray_image.shape[1], x + width + padding)
    y1 = min(gray_image.shape[0], y + height + padding)
    return gray_image[y0:y1, x0:x1]


def _ensure_rgb(image_array: np.ndarray):
    if image_array.ndim == 2:
        return cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)
    return image_array


def _build_ocr_variants(image: Image.Image):
    """
    Returns 2 variants instead of 4 to cut peak RAM usage by ~50%.
    - cropped_rgb: clean colour crop, works well for printed/typed math
    - thresholded: high-contrast binary, works well for handwritten/noisy math
    upscaled_gray and adaptive are dropped; they added marginal OCR quality
    but each carried a full beamsearch pass worth of RAM overhead.
    """
    rgb_image = np.array(image.convert("RGB"))
    gray_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2GRAY)
    cropped = _crop_foreground(gray_image)
    crop_box = image.getbbox() or (0, 0, image.width, image.height)
    cropped_rgb = np.array(image.crop(crop_box).convert("RGB"))
    denoised = cv2.fastNlMeansDenoising(cropped, None, 15, 7, 21)
    upscaled = cv2.resize(
        denoised,
        None,
        fx=3.0,
        fy=3.0,
        interpolation=cv2.INTER_CUBIC,
    )

    if float(upscaled.mean()) < 140:
        upscaled = 255 - upscaled

    sharpen_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened = cv2.filter2D(upscaled, -1, sharpen_kernel)
    _, thresholded = cv2.threshold(
        sharpened,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )

    return [
        ("cropped_rgb", _ensure_rgb(cropped_rgb)),
        ("thresholded", _ensure_rgb(thresholded)),
    ]


def _sort_ocr_results(results):
    entries = []
    for item in results:
        if len(item) < 3:
            continue

        bbox, text, confidence = item
        if not str(text).strip():
            continue

        xs = [point[0] for point in bbox]
        ys = [point[1] for point in bbox]
        entries.append(
            {
                "text": str(text).strip(),
                "confidence": float(confidence),
                "x": min(xs),
                "y": min(ys),
                "height": max(ys) - min(ys),
            }
        )

    entries.sort(key=lambda entry: (entry["y"], entry["x"]))
    if not entries:
        return []

    lines = []
    current_line = [entries[0]]
    current_y = entries[0]["y"]
    current_height = max(entries[0]["height"], 1)

    for entry in entries[1:]:
        line_tolerance = max(12, current_height * 0.6)
        if abs(entry["y"] - current_y) <= line_tolerance:
            current_line.append(entry)
            current_height = max(current_height, entry["height"])
            continue

        lines.append(current_line)
        current_line = [entry]
        current_y = entry["y"]
        current_height = max(entry["height"], 1)

    lines.append(current_line)
    return lines


def _assemble_ocr_text(results):
    lines = _sort_ocr_results(results)
    if not lines:
        return "", 0.0

    extracted_lines = []
    confidence_scores = []

    for line in lines:
        line.sort(key=lambda entry: entry["x"])
        extracted_lines.append(" ".join(entry["text"] for entry in line))
        confidence_scores.extend(entry["confidence"] for entry in line)

    confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
    return "\n".join(extracted_lines).strip(), confidence


def _score_ocr_candidate(text: str, confidence: float):
    normalized = text.strip().lower()
    if not normalized:
        return -1.0

    score = confidence * 4
    score += min(len(normalized), 120) / 120
    for marker in ("lim", "sin", "cos", "tan", "log", "ln", "sqrt", "^", "/", "=", "x", "e^"):
        if marker in normalized:
            score += 0.25

    if normalized.count("_") > 2:
        score -= 0.4
    if normalized.count("?") > 2:
        score -= 0.4
    if normalized.count("determinant") and "lim" in normalized:
        score -= 1.0

    return score


def _looks_like_noisy_math_ocr(text: str):
    normalized = text.strip().lower()
    if not normalized:
        return True

    if any(pattern in normalized for pattern in NOISY_OCR_PATTERNS):
        return True

    if "lim" in normalized and "x->0" not in normalized:
        return True

    if "lim" in normalized and "e^z" in normalized and "x" in normalized:
        return True

    if re.search(r"/\s*\d+\s+[xyz]\^[0-9]+\b", normalized):
        return True

    if (
        "lim x->0" in normalized
        and re.search(r"[+\-].+[xyz]\^[0-9]+\s*$", normalized)
        and not re.search(r"/\s*[xyz]\^[0-9]+\b", normalized)
    ):
        return True

    if "evaluate" in normalized and len(normalized.split()) <= 4:
        return True

    return False


def _repair_math_ocr_candidates(candidates):
    unique_texts = []
    for candidate in candidates:
        text = candidate["text"]
        if text not in unique_texts:
            unique_texts.append(text)
        if len(unique_texts) >= MAX_OCR_ALTERNATIVES:
            break

    if not unique_texts:
        return None

    try:
        repair_llm = _get_ocr_repair_llm()
        result = invoke_json_model(
            repair_llm,
            [
                SystemMessage(
                    content=(
                        "You repair noisy OCR extracted from a single JEE math question image. "
                        "Return one plain-text problem statement in ASCII math notation. "
                        "Preserve the original problem type. "
                        "Prefer standard forms like 'Evaluate the limit lim x->0 (...) / (...)'. "
                        "Use x^2, x^3, e^x, sin x, cos x, ln(1+x), sqrt x. "
                        "Do not invent a different topic or unrelated numbers. "
                        "If the OCR is imperfect, make the most conservative mathematically standard reconstruction."
                    )
                ),
                HumanMessage(
                    content=(
                        "OCR candidates from the same image:\n"
                        + "\n".join(
                            f"{index}. {text}" for index, text in enumerate(unique_texts, start=1)
                        )
                    )
                ),
            ],
            OCRRepairOutput,
            "Return a JSON object with exactly these keys: text (string), confidence (number from 0 to 1).",
        )
    except Exception:  # noqa: BLE001
        return None

    repaired_text = _normalize_math_ocr_text(result.text)
    if not repaired_text:
        return None

    return {
        "variant": "llm_repair",
        "text": repaired_text,
        "confidence": max(candidate["confidence"] for candidate in candidates),
        "applied_corrections": ["llm_math_reconstruction"],
        "score": _score_ocr_candidate(repaired_text, result.confidence) + 0.35,
    }


def _run_ocr_on_variant(reader, variant_image, use_beamsearch: bool = False):
    """
    Runs EasyOCR on a single variant.
    - Default: greedy decoder (fast, low RAM — ~3x less than beamsearch)
    - use_beamsearch=True: only called for a targeted retry on low-confidence results
    """
    return reader.readtext(
        variant_image,
        detail=1,
        paragraph=False,
        allowlist=MATH_ALLOWLIST,
        decoder="beamsearch" if use_beamsearch else "greedy",
        canvas_size=2048,   # was 4096 — halves memory for large images
        mag_ratio=1.5,      # was 2.0 — reduces intermediate array sizes
        text_threshold=0.5,
        low_text=0.25,
        link_threshold=0.2,
    )


def extract_text_from_image(file_bytes: bytes) -> ExtractionResponse:
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    reader = _get_ocr_reader()
    candidates = []

    for variant_name, variant_image in _build_ocr_variants(image):
        # First pass: greedy decoder — fast and memory-efficient
        results = _run_ocr_on_variant(reader, variant_image, use_beamsearch=False)
        extracted_text, confidence = _assemble_ocr_text(results)
        corrected_text, applied_corrections = _apply_runtime_corrections(extracted_text)
        score = _score_ocr_candidate(corrected_text, confidence)
        if not corrected_text:
            continue

        candidates.append(
            {
                "variant": variant_name,
                "text": corrected_text,
                "confidence": confidence,
                "applied_corrections": applied_corrections,
                "score": score,
            }
        )

    if not candidates:
        return ExtractionResponse(
            input_type="image",
            text="",
            confidence=0.0,
            requires_human_review=True,
            applied_corrections=[],
            alternatives=[],
        )

    candidates.sort(key=lambda item: item["score"], reverse=True)
    best_candidate = candidates[0]
    raw_confidence = best_candidate["confidence"]

    # Only retry with beamsearch on the single best variant if confidence is low.
    # This avoids running beamsearch across all variants while still recovering
    # difficult images.
    if raw_confidence < 0.85 or _looks_like_noisy_math_ocr(best_candidate["text"]):
        best_variant_image = dict(_build_ocr_variants(image)).get(best_candidate["variant"])
        if best_variant_image is not None:
            beam_results = _run_ocr_on_variant(reader, best_variant_image, use_beamsearch=True)
            beam_text, beam_confidence = _assemble_ocr_text(beam_results)
            beam_corrected, beam_corrections = _apply_runtime_corrections(beam_text)
            beam_score = _score_ocr_candidate(beam_corrected, beam_confidence)
            if beam_corrected and beam_score > best_candidate["score"]:
                candidates.append(
                    {
                        "variant": f"{best_candidate['variant']}_beam",
                        "text": beam_corrected,
                        "confidence": beam_confidence,
                        "applied_corrections": beam_corrections,
                        "score": beam_score,
                    }
                )

        repaired_candidate = _repair_math_ocr_candidates(candidates)
        if repaired_candidate is not None:
            candidates.append(repaired_candidate)

        candidates.sort(key=lambda item: item["score"], reverse=True)
        best_candidate = candidates[0]

    alternatives = []
    for candidate in candidates:
        text = candidate["text"]
        if text not in alternatives:
            alternatives.append(text)
        if len(alternatives) >= MAX_OCR_ALTERNATIVES:
            break

    return ExtractionResponse(
        input_type="image",
        text=best_candidate["text"],
        confidence=round(raw_confidence, 3),
        requires_human_review=raw_confidence < 0.75,
        applied_corrections=best_candidate["applied_corrections"],
        alternatives=alternatives,
    )


def _estimate_asr_confidence(transcript_result: dict):
    segments = transcript_result.get("segments", [])
    if not segments:
        return 0.0

    avg_logprob = sum(segment.get("avg_logprob", -5.0) for segment in segments) / len(segments)
    confidence = max(0.0, min(1.0, 1.0 + (avg_logprob / 5.0)))
    return confidence


def transcribe_audio(file_bytes: bytes, filename: str) -> ExtractionResponse:
    suffix = Path(filename).suffix or ".wav"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(file_bytes)
        temp_path = temp_file.name

    try:
        model = _get_whisper_model()
        result = model.transcribe(temp_path, fp16=False)
    finally:
        Path(temp_path).unlink(missing_ok=True)

    transcript = (result.get("text") or "").strip()
    confidence = _estimate_asr_confidence(result)
    corrected_text, applied_corrections = _apply_runtime_corrections(transcript)

    return ExtractionResponse(
        input_type="audio",
        text=corrected_text,
        confidence=round(confidence, 3),
        requires_human_review=confidence < 0.75,
        applied_corrections=applied_corrections,
        alternatives=[],
    )
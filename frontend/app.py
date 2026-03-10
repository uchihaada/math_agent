import json

import requests
import streamlit as st

API_DEFAULT = "https://math-agent-6ha8.onrender.com"
ACTIVE_WORKFLOW_STATUSES = {"accepted", "queued", "running"}
TERMINAL_WORKFLOW_STATUSES = {"success", "rejected", "error"}
REVIEW_ACTIONS = {
    "input_review": [
        ("Approve Text", "approve"),
        ("Edit and Continue", "edit"),
        ("Reject", "reject"),
    ],
    "parser_review": [
        ("Approve Parse", "approve"),
        ("Edit and Re-run Parser", "edit"),
        ("Reject", "reject"),
    ],
    "solver_review": [
        ("Approve Solution", "approve"),
        ("Edit and Re-solve", "edit"),
        ("Recheck Solver", "recheck"),
        ("Reject", "reject"),
    ],
    "final_review": [
        ("Approve Final", "approve"),
        ("Edit Final Answer", "edit"),
        ("Recheck Solver", "recheck"),
        ("Reject", "reject"),
    ],
}


def _init_state():
    st.session_state.setdefault("api_base", API_DEFAULT)
    st.session_state.setdefault("response", None)
    st.session_state.setdefault("thread_id", None)
    st.session_state.setdefault("polling", False)
    st.session_state.setdefault("user_text", "")
    st.session_state.setdefault("pending_user_text", None)
    st.session_state.setdefault("extraction", None)
    st.session_state.setdefault("extracted_text", "")
    st.session_state.setdefault("pending_extracted_text", None)
    st.session_state.setdefault("pending_review_reset", False)
    st.session_state.setdefault("review_feedback", "")
    st.session_state.setdefault("review_stage", None)
    st.session_state.setdefault("feedback_comment", "")
    st.session_state.setdefault("feedback_result", None)
    st.session_state.setdefault("feedback_interaction_id", None)
    st.session_state.setdefault("ocr_candidate", "")


def _apply_pending_widget_updates():
    if st.session_state.pending_user_text is not None:
        st.session_state.user_text = st.session_state.pending_user_text
        st.session_state.pending_user_text = None

    if st.session_state.pending_extracted_text is not None:
        st.session_state.extracted_text = st.session_state.pending_extracted_text
        st.session_state.pending_extracted_text = None

    if st.session_state.pending_review_reset:
        st.session_state.review_feedback = ""
        st.session_state.review_stage = None
        st.session_state.pending_review_reset = False


def _reset_review_state():
    st.session_state.pending_review_reset = True


def _reset_feedback_state():
    st.session_state.feedback_comment = ""
    st.session_state.feedback_result = None
    st.session_state.feedback_interaction_id = None


def _is_workflow_locked():
    response = st.session_state.response or {}
    status = response.get("status")
    return bool(st.session_state.thread_id) and status not in TERMINAL_WORKFLOW_STATUSES


def _decode_response(response):
    try:
        payload = response.json()
    except ValueError:
        payload = {
            "status": "error",
            "message": response.text or f"HTTP {response.status_code}",
        }

    if not isinstance(payload, dict):
        payload = {"status": "error", "message": str(payload)}

    if "detail" in payload and "message" not in payload:
        detail = payload["detail"]
        payload["message"] = (
            json.dumps(detail)
            if isinstance(detail, (dict, list))
            else str(detail)
        )

    if not response.ok:
        payload["status"] = "error"
        payload.setdefault("message", f"HTTP {response.status_code}")

    payload.setdefault("status", "success")
    return payload


def _request(method, path, *, json_payload=None, files=None, timeout=120):
    try:
        response = requests.request(
            method,
            f"{st.session_state.api_base}{path}",
            json=json_payload,
            files=files,
            timeout=timeout,
        )
        return _decode_response(response)
    except requests.RequestException as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


def _post_json(path, payload):
    return _request("POST", path, json_payload=payload, timeout=120)


def _get_json(path):
    return _request("GET", path, timeout=30)


def _post_file(path, uploaded_file):
    return _request(
        "POST",
        path,
        files={
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream",
            )
        },
        timeout=300,
    )


def _coerce_display_value(value):
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            try:
                return json.loads(stripped)
            except json.JSONDecodeError:
                return value
    return value


def _format_label(label):
    return str(label).replace("_", " ").strip().title()


def _render_simple_value(value):
    value = _coerce_display_value(value)

    if isinstance(value, dict):
        for key, item in value.items():
            item = _coerce_display_value(item)
            if isinstance(item, (dict, list)):
                with st.expander(_format_label(key), expanded=False):
                    _render_simple_value(item)
            else:
                rendered = str(item).strip() if item is not None else "None"
                if "\n" in rendered:
                    st.markdown(f"**{_format_label(key)}**")
                    st.markdown(rendered.replace("\n", "  \n"))
                else:
                    st.markdown(f"**{_format_label(key)}:** {rendered}")
        return

    if isinstance(value, list):
        if not value:
            st.write("None")
            return

        if all(not isinstance(item, (dict, list)) for item in value):
            st.write(", ".join(str(item) for item in value))
            return

        for index, item in enumerate(value, start=1):
            with st.expander(f"Item {index}", expanded=False):
                _render_simple_value(item)
        return

    rendered = str(value).strip() if value is not None else "None"
    if "\n" in rendered:
        st.markdown(rendered.replace("\n", "  \n"))
    else:
        st.write(rendered)


def _render_verification_block(verification):
    verification = _coerce_display_value(verification)
    if not verification:
        return

    st.subheader("Verification")
    if isinstance(verification, dict):
        is_correct = verification.get("is_correct")
        confidence = verification.get("confidence")
        issues = verification.get("issues")

        if is_correct is not None:
            st.markdown(f"**Correct:** {'Yes' if is_correct else 'No'}")
        if confidence is not None:
            st.markdown(f"**Confidence:** {float(confidence):.2%}")
        if issues:
            st.markdown("**Issues:**")
            for issue in issues:
                st.write(f"- {issue}")
        return

    _render_simple_value(verification)


def _render_hitl_details(stage, details):
    details = _coerce_display_value(details or {})
    if not isinstance(details, dict):
        _render_simple_value(details)
        return

    if stage in {"input_review", "parser_review"}:
        if details.get("input_text"):
            st.subheader("Current Input")
            st.markdown(str(details["input_text"]).replace("\n", "  \n"))

        if details.get("parsed_problem"):
            with st.expander("Parsed Problem", expanded=True):
                _render_simple_value(details["parsed_problem"])

        if details.get("ocr_confidence") is not None:
            st.markdown(f"**OCR Confidence:** {float(details['ocr_confidence']):.2%}")
        if details.get("asr_confidence") is not None:
            st.markdown(f"**ASR Confidence:** {float(details['asr_confidence']):.2%}")
        return

    if stage == "solver_review":
        if details.get("problem"):
            st.subheader("Problem")
            st.markdown(str(details["problem"]).replace("\n", "  \n"))
        if details.get("candidate_solution"):
            st.subheader("Candidate Solution")
            st.markdown(str(details["candidate_solution"]).replace("\n", "  \n"))
        _render_verification_block(details.get("verification"))
        return

    if stage == "final_review":
        if details.get("problem"):
            st.subheader("Problem")
            st.markdown(str(details["problem"]).replace("\n", "  \n"))
        if details.get("solution"):
            st.subheader("Proposed Final Solution")
            st.markdown(str(details["solution"]).replace("\n", "  \n"))
        if details.get("explanation"):
            with st.expander("Explanation", expanded=True):
                st.markdown(str(details["explanation"]).replace("\n", "  \n"))
        _render_verification_block(details.get("verification"))
        return

    _render_simple_value(details)


def _run_extraction(mode, uploaded_file):
    path = "/extract/image" if mode == "Image" else "/extract/audio"
    extraction = _post_file(path, uploaded_file)
    st.session_state.response = None
    st.session_state.thread_id = None
    st.session_state.polling = False
    _reset_review_state()
    _reset_feedback_state()

    if extraction.get("status") == "error":
        st.session_state.extraction = None
        st.error(extraction["message"])
        return

    st.session_state.extraction = extraction
    st.session_state.extracted_text = extraction["text"]
    st.session_state.ocr_candidate = extraction["text"]


def _start_solve(mode, text):
    extraction = st.session_state.extraction or {}
    payload = {
        "input_type": mode.lower(),
        "text": text,
        "ocr_confidence": extraction.get("confidence") if mode == "Image" else None,
        "asr_confidence": extraction.get("confidence") if mode == "Audio" else None,
        "input_reviewed": mode in {"Image", "Audio"} and bool(extraction),
    }
    _reset_review_state()
    _reset_feedback_state()
    st.session_state.response = _post_json("/solve/start", payload)
    st.session_state.thread_id = st.session_state.response.get("thread_id")
    st.session_state.polling = (
        st.session_state.response.get("status") in ACTIVE_WORKFLOW_STATUSES
    )
    st.rerun()


def _resume_review(action):
    response = st.session_state.response or {}
    stage = response.get("stage")
    feedback = st.session_state.review_feedback or None

    if action == "edit" and feedback:
        if stage in {"input_review", "parser_review"}:
            # For input/parser review, feedback is corrected input text
            st.session_state.pending_user_text = feedback
            st.session_state.pending_extracted_text = feedback
        elif stage in {"solver_review", "final_review"}:
            # For solver/final review, also preserve as extracted text if it was corrected
            st.session_state.pending_extracted_text = feedback

    payload = {
        "thread_id": st.session_state.thread_id,
        "review": {
            "stage": stage,
            "action": action,
            "feedback": feedback,
        },
    }
    st.session_state.response = _post_json("/solve/start", payload)
    st.session_state.thread_id = st.session_state.response.get("thread_id")
    st.session_state.polling = (
        st.session_state.response.get("status") in ACTIVE_WORKFLOW_STATUSES
    )
    st.session_state.feedback_result = None
    st.session_state.feedback_interaction_id = None

    if st.session_state.response.get("status") != "hitl_required":
        _reset_review_state()
    st.rerun()


def _fetch_status():
    if not st.session_state.thread_id:
        return False

    previous_status = (st.session_state.response or {}).get("status")
    st.session_state.response = _get_json(
        f"/solve/status/{st.session_state.thread_id}"
    )
    st.session_state.polling = (
        st.session_state.response.get("status") in ACTIVE_WORKFLOW_STATUSES
    )
    return previous_status != st.session_state.response.get("status")


def _submit_feedback(is_correct):
    response = st.session_state.response or {}
    interaction_id = response.get("interaction_id")
    if interaction_id is None:
        st.error("No completed interaction is available for feedback.")
        return

    result = _post_json(
        "/feedback",
        {
            "interaction_id": interaction_id,
            "is_correct": is_correct,
            "comment": st.session_state.feedback_comment or None,
        },
    )

    if result.get("status") == "error":
        st.error(result["message"])
        return

    st.session_state.feedback_result = result["feedback_type"]
    st.session_state.feedback_interaction_id = interaction_id
    if not is_correct:
        st.session_state.feedback_comment = ""
    st.rerun()


def _render_trace(trace, current_agent=None):
    if not trace and not current_agent:
        return

    st.subheader("Agent Trace")
    for index, step in enumerate(trace, start=1):
        with st.expander(
            f"{index}. {step['agent']} - {step['action']}",
            expanded=index == len(trace),
        ):
            st.caption(step["reason"])
            if step.get("output"):
                _render_simple_value(step["output"])

    if current_agent:
        st.info(f"Running now: {current_agent}")


def _render_retrieved_context(items):
    if not items:
        return

    with st.expander("Retrieved Context", expanded=False):
        for item in items:
            source = item.get("source") or "unknown"
            topic = item.get("topic") or "n/a"
            doc_type = item.get("doc_type") or "context"
            st.markdown(f"**{doc_type}** | topic: `{topic}` | source: `{source}`")
            st.code(item.get("content", ""), language="markdown")


def _sync_review_feedback(response):
    stage = response.get("stage")
    if not stage or st.session_state.review_stage == stage:
        return

    details = response.get("details", {})
    default_feedback = ""

    if stage in {"input_review", "parser_review"}:
        default_feedback = details.get("input_text", "")
    elif stage == "final_review":
        default_feedback = details.get("solution", "")
    elif stage == "solver_review":
        default_feedback = details.get("candidate_solution", "")

    st.session_state.review_feedback = default_feedback
    st.session_state.review_stage = stage


def _render_response():
    response = st.session_state.response
    if not response:
        return

    status = response.get("status")
    current_agent = response.get("current_agent")
    trace_col, result_col = st.columns([1, 2], gap="large")

    with trace_col:
        _render_trace(response.get("trace", []), current_agent=current_agent)

    with result_col:
        if status in ACTIVE_WORKFLOW_STATUSES:
            st.info(response.get("message", "Workflow is running."))
            st.caption(
                f"Thread: {response.get('thread_id')} | Current: {current_agent or 'waiting'}"
            )
            _render_retrieved_context(response.get("retrieved_context", []))
            return

        if status == "hitl_required":
            _sync_review_feedback(response)
            stage = response["stage"]
            actions = REVIEW_ACTIONS.get(stage, [("Reject", "reject")])

            st.warning(response["message"])
            st.caption(f"Stage: {stage} | Thread: {response['thread_id']}")
            _render_hitl_details(stage, response.get("details", {}))
            _render_retrieved_context(response.get("retrieved_context", []))

            st.text_area(
                "Review feedback / edited text",
                key="review_feedback",
                help="Use this for corrected OCR or ASR text, parser clarification, solver feedback, or final answer edits.",
            )

            review_cols = st.columns(len(actions))
            for idx, (label, action) in enumerate(actions):
                if review_cols[idx].button(label):
                    _resume_review(action)
            return

        if status == "rejected":
            st.error(response["message"])
            return

        if status == "error":
            st.error(response.get("message", "Unknown workflow error."))
            _render_retrieved_context(response.get("retrieved_context", []))
            return

        st.success("Solved")
        st.caption(
            f"Thread: {response['thread_id']} | Interaction: {response.get('interaction_id')}"
        )

        confidence = float(response.get("confidence", 0.0))
        st.metric("Confidence", f"{confidence:.2%}")
        st.progress(min(max(confidence, 0.0), 1.0))

        st.subheader("Final Answer")
        st.markdown(str(response.get("solution", "")).replace("\n", "  \n"))

        st.subheader("Explanation")
        st.markdown(str(response.get("explanation", "")).replace("\n", "  \n"))

        _render_retrieved_context(response.get("retrieved_context", []))

        with st.expander("Verification", expanded=False):
            _render_verification_block(response.get("verification", {}))

        interaction_id = response.get("interaction_id")
        feedback_saved = (
            interaction_id is not None
            and st.session_state.feedback_interaction_id == interaction_id
            and st.session_state.feedback_result is not None
        )

        final_action = response.get("final_action")
        if feedback_saved:
            st.success(f"Feedback saved: {st.session_state.feedback_result}")
            return

        if final_action in {"approve", "edit"}:
            action_label = "approved" if final_action == "approve" else "approved after edit"
            st.info(
                f"Final review already recorded this solution as {action_label}. "
                "Use the field below only if you want to report that the saved answer is still incorrect."
            )
            st.text_input("Issue comment", key="feedback_comment")
            if st.button("Report Incorrect"):
                _submit_feedback(False)
            return

        st.text_input("Feedback comment", key="feedback_comment")
        feedback_cols = st.columns(2)
        if feedback_cols[0].button("Correct"):
            _submit_feedback(True)
        if feedback_cols[1].button("Incorrect"):
            _submit_feedback(False)


@st.fragment(run_every=2)
def _poll_workflow_status():
    if st.session_state.polling and st.session_state.thread_id:
        status_changed = _fetch_status()
        if status_changed:
            st.rerun()
    _render_response()


st.set_page_config(page_title="AI Math Mentor", layout="wide")
_init_state()
_apply_pending_widget_updates()
st.title("AI Math Mentor")

with st.sidebar:
    st.text_input("API Base URL", key="api_base")
    if st.button("Health Check"):
        health = _get_json("/health")
        if health.get("status") == "error":
            st.error(health["message"])
        else:
            st.success(health["status"])

workflow_locked = _is_workflow_locked()
mode = st.selectbox("Input Mode", ["Text", "Image", "Audio"], disabled=workflow_locked)

if mode == "Text":
    user_text = st.text_area(
        "Enter your math problem",
        key="user_text",
        height=180,
        disabled=workflow_locked,
    )
    if st.button("Solve Text", disabled=workflow_locked):
        _start_solve(mode, user_text)

elif mode == "Image":
    image_file = st.file_uploader(
        "Upload JPG/PNG",
        type=["jpg", "jpeg", "png"],
        disabled=workflow_locked,
    )
    if image_file is not None:
        st.image(image_file, caption="Uploaded image", use_container_width=True)
        if st.button("Run OCR", disabled=workflow_locked):
            _run_extraction(mode, image_file)

    if st.session_state.extraction and st.session_state.extraction.get("input_type") == "image":
        extraction = st.session_state.extraction
        if workflow_locked:
            st.caption("OCR was already submitted to the workflow. Continue with the review panel below.")
        else:
            st.metric("OCR Confidence", f"{float(extraction['confidence']):.2%}")
            if extraction["requires_human_review"]:
                st.warning("OCR confidence is low. Review the extracted text before solving.")
            if extraction.get("applied_corrections"):
                st.info(
                    "Applied learned corrections: "
                    + ", ".join(extraction["applied_corrections"])
                )
            alternatives = extraction.get("alternatives") or []
            if alternatives:
                selected_candidate = st.selectbox(
                    "OCR Candidate",
                    alternatives,
                    key="ocr_candidate",
                )

                if st.button("Use OCR Candidate"):
                    st.session_state.extracted_text = selected_candidate
            extracted_text_value = st.text_area("Extracted Text", key="extracted_text", height=180)

            if st.button("Solve Image Problem"):
                _start_solve(mode, extracted_text_value)

else:
    audio_recording = st.audio_input("Record audio", disabled=workflow_locked)
    uploaded_audio = st.file_uploader(
        "Or upload audio",
        type=["wav", "mp3", "m4a"],
        disabled=workflow_locked,
    )
    audio_file = audio_recording or uploaded_audio

    if audio_file is not None and st.button("Transcribe Audio", disabled=workflow_locked):
        _run_extraction(mode, audio_file)

    if st.session_state.extraction and st.session_state.extraction.get("input_type") == "audio":
        extraction = st.session_state.extraction
        if workflow_locked:
            st.caption("Transcript was already submitted to the workflow. Continue with the review panel below.")
        else:
            st.metric("ASR Confidence", f"{float(extraction['confidence']):.2%}")
            if extraction["requires_human_review"]:
                st.warning("Transcription confidence is low. Review the transcript before solving.")
            if extraction.get("applied_corrections"):
                st.info(
                    "Applied learned corrections: "
                    + ", ".join(extraction["applied_corrections"])
                )
            transcript_value = st.text_area("Transcript", key="extracted_text", height=180)
            if st.button("Solve Audio Problem"):
                st.session_state.pending_extracted_text = transcript_value
                _start_solve(mode, transcript_value)

_poll_workflow_status()

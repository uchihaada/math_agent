from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.agents.extraction_agent import extract_text_from_image, transcribe_audio
from backend.app.workflow import WorkflowController
from backend.memory.memory_store import save_feedback
from backend.models.schemas import FeedbackRequest, SolveRequest

router = APIRouter()
workflow = WorkflowController()


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/extract/image")
async def extract_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Image filename is required.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded image is empty.")

    result = extract_text_from_image(file_bytes)
    return result.model_dump()


@router.post("/extract/audio")
async def extract_audio(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Audio filename is required.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded audio is empty.")

    result = transcribe_audio(file_bytes, file.filename)
    return result.model_dump()


@router.post("/solve")
async def solve(request: SolveRequest):
    return workflow.run(request)


@router.post("/solve/start")
async def solve_start(request: SolveRequest):
    return workflow.run_async(request)


@router.get("/solve/status/{thread_id}")
async def solve_status(thread_id: str):
    return workflow.get_status(thread_id)


@router.post("/feedback")
async def feedback(request: FeedbackRequest):
    feedback_type = "user_correct" if request.is_correct else "user_incorrect"
    save_feedback(request.interaction_id, feedback_type=feedback_type, comment=request.comment)
    return {"status": "saved", "feedback_type": feedback_type}

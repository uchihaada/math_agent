from fastapi import FastAPI

from backend.api.routes import router
from backend.memory.database import init_db

app = FastAPI(title="Math Mentor AI")

init_db()

app.include_router(router)


@app.get("/")
def home():
    return {"message": "Math Mentor API running"}

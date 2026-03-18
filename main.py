from fastapi import FastAPI
from controller.match_controller import router

app = FastAPI(
    title="AI Resume Matcher",
    version="1.0.0"
)

app.include_router(router)
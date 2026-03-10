from dotenv import load_dotenv

load_dotenv()

from backend.core.logging import configure_logging

configure_logging()

from fastapi import FastAPI

from backend.api.generation import router as generation_router
from backend.api.posts import router as posts_router
from backend.middleware.logging_middleware import RequestLoggingMiddleware

app = FastAPI()
app.add_middleware(RequestLoggingMiddleware)

app.include_router(generation_router, prefix="/api/v1")
app.include_router(posts_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "ok"}

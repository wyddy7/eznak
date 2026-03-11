from contextlib import asynccontextmanager

from dotenv import load_dotenv

load_dotenv()

from backend.core.logging import configure_logging

configure_logging()

import structlog
from fastapi import FastAPI

from backend.api.channels import router as channels_router
from backend.api.generation import router as generation_router
from backend.api.posts import router as posts_router
from backend.middleware.logging_middleware import RequestLoggingMiddleware
from backend.services.scheduler import scheduler, setup_scheduler

log = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_scheduler()
    scheduler.start()
    log.info("scheduler_started")
    yield
    scheduler.shutdown(wait=True)


app = FastAPI(lifespan=lifespan)
app.add_middleware(RequestLoggingMiddleware)

app.include_router(channels_router, prefix="/api/v1")
app.include_router(generation_router, prefix="/api/v1")
app.include_router(posts_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"status": "ok"}

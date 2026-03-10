from dotenv import load_dotenv

load_dotenv()

from backend.core.logging import configure_logging

configure_logging()

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok"}

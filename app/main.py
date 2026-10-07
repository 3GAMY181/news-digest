from fastapi import FastAPI

from app.db import get_history, init_db
from app.news import build_digest

init_db()

app = FastAPI(title="News Digest API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/digest")
def digest(limit: int = 10):
    return build_digest(limit)


@app.get("/history")
def history(limit: int = 20):
    return get_history(limit)
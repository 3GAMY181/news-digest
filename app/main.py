from fastapi import FastAPI

from app.news import build_digest

app = FastAPI(title="News Digest API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/digest")
def digest(limit: int = 10):
    return build_digest(limit)
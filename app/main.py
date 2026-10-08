from fastapi import FastAPI

from app.db import get_history, init_db
from app.news import build_digest
from fastapi import Request
from fastapi.templating import Jinja2Templates

init_db()

app = FastAPI(title="News Digest API")
templates = Jinja2Templates(directory="app/templates")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/digest")
def digest(limit: int = 5):
    return build_digest(limit)


@app.get("/history")
def history(limit: int = 20):
    return get_history(limit)

@app.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(request, "index.html")
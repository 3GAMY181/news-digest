# News Digest

AI-powered news digest built with Python and n8n.

## Status

v0.1: Python script that fetches the latest tech news from an RSS feed.

v0.2: FastAPI endpoints + n8n workflow that sends the digest to Telegram.

v0.3: SQLite storage to avoid sending duplicate news.

## Roadmap
- [x] v0.1: Fetch news from RSS
- [x] v0.2: FastAPI + n8n workflow (send digest to Telegram)
- [x] v0.3: Store news in a database, avoid duplicates
- [ ] v0.4: Summarize and classify news with an LLM
- [ ] v0.5: Docker + docker-compose
- [ ] v0.6: Tests + GitHub Actions
- [ ] v1.0: Dashboard + full documentation

## Setup
    python -m venv venv
    venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python app/main.py

## n8n Workflow
Import `n8n/workflow.json` from the n8n UI (Workflows → Import from File),
then set your own Telegram credentials and chat ID.

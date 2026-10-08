import re
import time

import feedparser

from app.db import filter_unseen, save_news
from app.llm import summarize_and_classify

FEEDS = [
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://techcrunch.com/feed/",
]

KEYWORDS = ["ai", "python", "openai", "google"]

# الـ free tier ليه حد طلبات في الدقيقة، فبنستنى بين كل خبر
PAUSE_SECONDS = 6


def fetch_news(feed_url):
    """بيجيب الأخبار من رابط RSS واحد"""
    feed = feedparser.parse(feed_url)
    news = []
    for entry in feed.entries:
        news.append(
            {
                "title": entry.title,
                "link": entry.link,
                "description": entry.get("summary", "")[:500],
            }
        )
    return news


def filter_news(news, keywords):
    """بيرجّع الأخبار اللي فيها كلمة مفتاحية كاملة (مش جزء من كلمة)"""
    pattern = re.compile(
        r"\b(" + "|".join(re.escape(k) for k in keywords) + r")\b",
        re.IGNORECASE,
    )
    return [item for item in news if pattern.search(item["title"])]


def format_digest(news):
    """بيحوّل الأخبار لنص جاهز للإرسال، مجمّعة حسب التصنيف"""
    if not news:
        return "مفيش أخبار جديدة النهارده."
    groups = {}
    for item in news:
        groups.setdefault(item["category"], []).append(item)
    lines = ["📰 ملخص الأخبار:\n"]
    for category, items in groups.items():
        lines.append(f"🔹 {category}")
        for item in items:
            lines.append(f"• {item['summary']}\n{item['link']}")
        lines.append("")
    return "\n".join(lines)


def build_digest(limit=5):
    all_news = []
    for url in FEEDS:
        all_news.extend(fetch_news(url))
    filtered = filter_news(all_news, KEYWORDS)
    unseen = filter_unseen(filtered)[:limit]

    enriched = []
    for i, item in enumerate(unseen):
        if i > 0:
            time.sleep(PAUSE_SECONDS)
        result = summarize_and_classify(item["title"], item.get("description", ""))
        if not result["ok"]:
            continue  # LLM failed: do not save, retry on the next run
        entry = {
            "title": item["title"],
            "link": item["link"],
            "summary": result["summary"],
            "category": result["category"],
        }
        save_news(entry)
        enriched.append(entry)

    return {
        "count": len(enriched),
        "items": enriched,
        "text": format_digest(enriched),
    }
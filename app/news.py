import feedparser

from app.db import save_new_news

FEEDS = [
    "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "https://techcrunch.com/feed/",
]

KEYWORDS = ["ai", "python", "openai", "google"]


def fetch_news(feed_url):
    """بيجيب الأخبار من رابط RSS واحد"""
    feed = feedparser.parse(feed_url)
    news = []
    for entry in feed.entries:
        news.append({"title": entry.title, "link": entry.link})
    return news


def filter_news(news, keywords):
    """بيرجّع بس الأخبار اللي فيها كلمة من الكلمات المفتاحية"""
    result = []
    for item in news:
        title = item["title"].lower()
        for word in keywords:
            if word in title:
                result.append(item)
                break
    return result


def format_digest(news):
    """بيحوّل الأخبار لنص جاهز للإرسال"""
    if not news:
        return "مفيش أخبار جديدة النهارده."
    lines = ["📰 ملخص الأخبار:\n"]
    for i, item in enumerate(news, start=1):
        lines.append(f"{i}. {item['title']}\n{item['link']}\n")
    return "\n".join(lines)


def build_digest(limit=10):
    all_news = []
    for url in FEEDS:
        all_news.extend(fetch_news(url))
    filtered = filter_news(all_news, KEYWORDS)[:limit]
    new_items = save_new_news(filtered)
    return {
        "count": len(new_items),
        "items": new_items,
        "text": format_digest(new_items),
    }
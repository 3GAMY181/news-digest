import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "news.db"


def get_connection():
    """بيفتح اتصال بقاعدة البيانات (وبيعمل مجلد data لو مش موجود)"""
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """بيعمل جدول الأخبار، وبيضيف عمودي الملخص والتصنيف لو ناقصين"""
    with closing(get_connection()) as conn:
        with conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL UNIQUE,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            existing = {row["name"] for row in conn.execute("PRAGMA table_info(news)")}
            if "summary" not in existing:
                conn.execute("ALTER TABLE news ADD COLUMN summary TEXT")
            if "category" not in existing:
                conn.execute("ALTER TABLE news ADD COLUMN category TEXT")


def save_new_news(news):
    """بيحفظ الأخبار الجديدة بس، وبيرجّع قايمة الأخبار اللي اتحفظت لأول مرة"""
    new_items = []
    with closing(get_connection()) as conn:
        with conn:
            for item in news:
                cursor = conn.execute(
                    "INSERT OR IGNORE INTO news (title, link) VALUES (?, ?)",
                    (item["title"], item["link"]),
                )
                if cursor.rowcount == 1:
                    new_items.append(item)
    return new_items


def filter_unseen(news):
    """بيرجّع الأخبار اللي لسه متخزنتش"""
    with closing(get_connection()) as conn:
        seen = {row["link"] for row in conn.execute("SELECT link FROM news")}
    return [item for item in news if item["link"] not in seen]


def save_news(item):
    """بيحفظ خبر واحد مع الملخص والتصنيف (لو موجودين)"""
    with closing(get_connection()) as conn:
        with conn:
            conn.execute(
                "INSERT OR IGNORE INTO news (title, link, summary, category) "
                "VALUES (?, ?, ?, ?)",
                (
                    item["title"],
                    item["link"],
                    item.get("summary"),
                    item.get("category"),
                ),
            )


def get_history(limit=20):
    """بيرجّع آخر الأخبار المحفوظة"""
    with closing(get_connection()) as conn:
        rows = conn.execute(
            "SELECT title, link, summary, category, created_at "
            "FROM news ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(row) for row in rows]
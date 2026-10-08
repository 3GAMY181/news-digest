import json
import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")
CATEGORIES = ["AI", "Security", "Tools", "Business", "Other"]
RETRIES = 4


def _generate(client, prompt):
    """بيكلّم الموديل، ولو فيه ضغط مؤقت بيستنى ويعيد"""
    for attempt in range(RETRIES):
        try:
            return client.models.generate_content(model=MODEL, contents=prompt)
        except (errors.ServerError, errors.ClientError) as e:
            code = getattr(e, "code", None)
            if code == 429 and "PerDay" in str(e):
                raise  # الحصة اليومية خلصت، الإعادة مالهاش لازمة
            retryable = code in (429, 500, 503)
            if not retryable or attempt == RETRIES - 1:
                raise
            time.sleep(2 ** (attempt + 1))  # 2 ثم 4 ثم 8 ثواني


def summarize_and_classify(title, description=""):
    """بياخد عنوان الخبر ووصفه، ويرجّع ملخص وتصنيف"""
    fallback = {"summary": title, "category": "Other", "ok": False}
    client = genai.Client()
    prompt = (
        "Summarize this news item in one short sentence and classify it.\n"
        f"Categories: {', '.join(CATEGORIES)}\n"
        f"Title: {title}\n"
        f"Description: {description}\n\n"
        'Reply with JSON only, like: {"summary": "...", "category": "AI"}'
    )
    try:
        response = _generate(client, prompt)
    except Exception as e:
        print(f"LLM unavailable, using fallback: {e}")
        return fallback

    text = (response.text or "").strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return fallback

    category = data.get("category")
    if category not in CATEGORIES:
        category = "Other"
    return {
        "summary": data.get("summary", title),
        "category": category,
        "ok": True,
    }


if __name__ == "__main__":
    print(summarize_and_classify("OpenAI releases a new model for developers"))
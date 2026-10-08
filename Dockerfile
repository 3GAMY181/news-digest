# استخدام نسخة بايثون خفيفة
FROM python:3.10-slim

# تحديد مسار العمل جوه الـ Container
WORKDIR /app

# نسخ ملف المتطلبات وتثبيت الحزم
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# تشغيل السيرفر
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
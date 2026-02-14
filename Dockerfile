FROM python:3.11-slim

# Системные зависимости для работы с PDF/OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    tesseract-ocr \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Ставим Docling прямо из GitHub
RUN pip install --no-cache-dir git+https://github.com/DS4SD/docling.git

# Ставим веб-фреймворк для API
RUN pip install --no-cache-dir fastapi uvicorn python-multipart

# Копируем файл с API
COPY app.py .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

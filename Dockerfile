# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/requirements.txt
# N?u b?n d� d? torch trong requirements, gi? nguy�n. Kh�ng c?n th�m CUDA v� Heroku kh�ng c� GPU.
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app

# N?u backend l� quiz_backend_fixed_v8.py v� Flask app t�n app
CMD ["gunicorn", "quiz_backend_fixed_v8:app", "--bind", "0.0.0.0:${PORT}", "--timeout", "120"]

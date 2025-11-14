# Build stage
FROM python:3.11-slim AS build
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt
COPY . .

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
RUN useradd -m appuser \
    && mkdir -p /app/db \
    && chown -R appuser:appuser /app \
    && apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
COPY --from=build /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=build /usr/local/bin /usr/local/bin
COPY . .
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
ENV PYTHONUNBUFFERED=1
USER appuser
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

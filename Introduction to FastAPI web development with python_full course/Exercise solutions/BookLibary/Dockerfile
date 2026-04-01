FROM python:3.12-slim
# Prevents .pyc files from being written to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures logs appear instantly in the terminal (no buffering)
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Create the folder for uploaded book cover images
RUN mkdir -p static/covers
EXPOSE 8000
# Run with gunicorn + 4 async workers for production
CMD ["gunicorn", "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", "--bind", "0.0.0.0:8000", "app.main:app"]
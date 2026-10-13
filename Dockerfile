# =============================================================================
# TrackIt — Parcel Tracking System (DevOps Laboratory Project)
# Module 4: Production Container Specification (Dockerfile)
# =============================================================================

# Step 1: Base Image (Lightweight, secure, official Python slim runtime)
FROM python:3.12-slim

# Step 2: Metadata labels
LABEL maintainer="College DevOps Laboratory Team"
LABEL project="TrackIt Parcel Tracking System"
LABEL version="1.0.0"
LABEL module="Module 4 — Docker Containerization & CI/CD"

# Step 3: Python runtime environment optimization
# Prevent writing .pyc bytecode to disk & ensure standard output is unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    FLASK_ENV=production

# Step 4: Set isolated working directory
WORKDIR /app

# Step 5: Install Python dependencies
# Copy requirements first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Step 6: Copy application code and test suites
COPY . /app/

# Step 7: Security Best Practice — Create and switch to non-root user
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --home /app appuser && \
    mkdir -p /app/data && \
    chown -R appuser:appgroup /app /app/data

USER appuser

# Step 8: Expose standard application port
EXPOSE 5000

# Step 9: Container Health Check
# Periodically verify the Flask application responds on port 5000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/')" || exit 1

# Step 10: Production WSGI Server Entrypoint
# Uses Gunicorn with 2 worker processes and 4 threads for concurrency
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "app:app"]

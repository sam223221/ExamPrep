# Software Maintenance Exam Prep — offline FastAPI + ChromaDB + bge-small image.
# Mirrors ExamPrep/cyper's offline pattern: CPU-only torch, the embedding model
# baked into the image, and HF offline flags so no network is touched at runtime.
# Multi-stage: a builder installs deps + downloads the model into HF_HOME, then a
# clean runtime stage copies only what's needed and runs as a non-root user.

# ---------- builder ----------
FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    HF_HOME=/models

WORKDIR /srv

# Install Python deps. CPU torch comes from the dedicated PyTorch wheel index so
# we never pull the (much larger) CUDA build into an offline, GPU-less image.
COPY requirements.txt .
RUN pip install --no-cache-dir torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

# Bake the embedding model into the image so runtime needs no network.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

# ---------- runtime ----------
FROM python:3.11-slim AS runtime

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    HF_HOME=/models \
    HF_HUB_OFFLINE=1 \
    TRANSFORMERS_OFFLINE=1 \
    PDF_ROOT=/data/pdfs \
    GUIDE_ROOT=/data/guides \
    MCQ_ROOT=/data/mcqs \
    CHROMA_DIR=/data/chroma_db \
    SLIDES_DIR=/data/slides \
    PORT=8000

# Non-root runtime user. The /data and /models trees are owned by it so the app,
# the slide cache, and the chroma volume are all writable without root.
RUN useradd --create-home --uid 10001 appuser \
 && mkdir -p /data/chroma_db /data/slides /models \
 && chown -R appuser:appuser /data /models

WORKDIR /srv

# Installed site-packages + console scripts (uvicorn) from the builder.
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
# The pre-downloaded embedding model.
COPY --from=builder --chown=appuser:appuser /models /models

# Application code (owned by the runtime user).
COPY --chown=appuser:appuser app ./app

USER appuser
EXPOSE 8000

# Liveness check hits the cheap /health route (no model load).
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0) if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=4).status==200 else sys.exit(1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

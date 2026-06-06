FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/models \
    PDF_ROOT=/data/pdfs \
    GUIDE_ROOT=/data/study-guide \
    CHROMA_DIR=/data/chroma_db

WORKDIR /srv
COPY app/requirements.txt .
RUN pip install --no-cache-dir torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt

# Bake the embedding model into the image so runtime is fully offline.
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('BAAI/bge-small-en-v1.5')"

ENV HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

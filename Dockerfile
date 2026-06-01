FROM python:3.11-slim AS lite-app

WORKDIR /app

COPY requirements.txt .
COPY src ./src
RUN chmod +x ./src/entrypoint.sh
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT ["./src/entrypoint.sh"]

FROM lite-app AS extended-app


COPY extended_src ./extended_src
RUN pip install --no-cache-dir -r extended_src/requirements.txt

ENV FASTEMBED_CACHE_PATH=/app/fastembed_cache
RUN python -c 'from fastembed import TextEmbedding; TextEmbedding(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")'


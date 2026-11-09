FROM python:3.12-slim

ARG WHISPER_VERSION=20250625

ENV PYTHONUNBUFFERED=1 \
    WHISPER_CACHE_DIR=/models

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir "openai-whisper==${WHISPER_VERSION#v}"

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh \
    && useradd --create-home --uid 1000 app \
    && mkdir -p /models \
    && chown app:app /models

COPY --chown=app:app main.py generate_session.py ./

USER app

ENTRYPOINT ["entrypoint.sh"]

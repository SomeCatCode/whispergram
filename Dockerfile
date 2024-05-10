FROM python:3

WORKDIR /app
USER root

ENV TELEGRAM_API_ID 0
ENV TELEGRAM_API_HASH 0
ENV WHISPER_MODEL "medium"

# Install dependencies
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade pip \
    && pip install -r requirements.txt \
    && pip install git+https://github.com/openai/whisper.git 

COPY . .
RUN mv entrypoint.sh /usr/local/bin/entrypoint.sh \
    && chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]

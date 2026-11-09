import asyncio
import logging
import os
import sys
import tempfile

import whisper
from telethon import TelegramClient, events
from telethon.sessions import StringSession

logging.basicConfig(level=logging.INFO)

MAX_MESSAGE_LENGTH = 4096
REPLY_PREFIX = "Autotranscription: "
SESSION_CHECK_TIMEOUT = 60


def fail(*messages):
    for message in messages:
        logging.error(message)
    sys.exit(1)


def read_int(name, value):
    try:
        return int(value)
    except ValueError:
        fail(f"{name} must be an integer.")


api_id = os.getenv("TELEGRAM_API_ID", "").strip()
api_hash = os.getenv("TELEGRAM_API_HASH", "").strip()
api_session = os.getenv("TELEGRAM_SESSION", "").strip()
telegram_user_id = os.getenv("TELEGRAM_USER_ID", "").strip()
model_name = os.getenv("WHISPER_MODEL", "medium").strip()
model_dir = os.getenv("WHISPER_CACHE_DIR") or None
blocked_list = os.getenv("BLOCKED_USERS_CHANNELS", "")

if not api_id or not api_hash:
    fail("TELEGRAM_API_ID and TELEGRAM_API_HASH must be set.")
api_id = read_int("TELEGRAM_API_ID", api_id)

if not api_session:
    fail(
        "TELEGRAM_SESSION is not set.",
        "Please set TELEGRAM_SESSION with docker compose run -it app python3 /app/generate_session.py",
    )

if not telegram_user_id:
    fail("TELEGRAM_USER_ID is not set.")
telegram_user_id = read_int("TELEGRAM_USER_ID", telegram_user_id)

blocked_users_and_channels = {
    read_int("BLOCKED_USERS_CHANNELS", entry.strip())
    for entry in blocked_list.split(",")
    if entry.strip()
}

logging.info(f"Used Model: {model_name}")
model = whisper.load_model(model_name, download_root=model_dir)
transcribe_lock = asyncio.Lock()


async def transcribe(file_path):
    async with transcribe_lock:
        result = await asyncio.to_thread(model.transcribe, file_path)
    return result["text"].strip()


async def handler(event):
    sender_id = event.sender_id

    if (telegram_user_id == 0 or sender_id == telegram_user_id) and event.raw_text == "?ID?":
        await event.reply(f"My ID: {sender_id}\nChat ID: {event.chat_id}")
        return

    message = event.message
    if not (message.voice or message.video_note):
        return

    if event.chat_id in blocked_users_and_channels or sender_id in blocked_users_and_channels:
        logging.info(f"Autotranscription disabled for chat {event.chat_id} / sender {sender_id}")
        return

    logging.info(f"Voicemessage received: {message.id}")
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = await event.client.download_media(message, file=temp_dir)
            if not file_path:
                logging.error(f"Download failed for message {message.id}")
                return
            text = await transcribe(file_path)
    except Exception:
        logging.exception(f"Transcription failed for message {message.id}")
        return

    if not text:
        logging.info(f"No speech detected in message {message.id}")
        return

    chunk_size = MAX_MESSAGE_LENGTH - len(REPLY_PREFIX)
    try:
        for i in range(0, len(text), chunk_size):
            await event.reply(REPLY_PREFIX + text[i : i + chunk_size])
    except Exception:
        logging.exception(f"Sending transcription failed for message {message.id}")


async def main():
    client = TelegramClient(StringSession(api_session), api_id, api_hash)
    await client.connect()
    try:
        authorized = await asyncio.wait_for(client.is_user_authorized(), timeout=SESSION_CHECK_TIMEOUT)
    except asyncio.TimeoutError:
        await client.disconnect()
        fail(
            f"Telegram did not answer within {SESSION_CHECK_TIMEOUT} seconds. TELEGRAM_SESSION may be invalid.",
            "Please create a new one with docker compose run -it app python3 /app/generate_session.py",
        )
    if not authorized:
        await client.disconnect()
        fail(
            "TELEGRAM_SESSION is invalid or expired.",
            "Please create a new one with docker compose run -it app python3 /app/generate_session.py",
        )

    client.add_event_handler(handler, events.NewMessage)
    logging.info("Bot started. Wait for voice messages...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())

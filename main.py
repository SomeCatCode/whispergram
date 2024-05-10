from telethon import TelegramClient, events
from telethon.sessions import StringSession
import whisper
import os
import logging

logging.basicConfig(level=logging.INFO)

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
api_session = os.getenv("TELEGRAM_SESSION")
model_name = os.getenv("WHISPER_MODEL", "medium")
model = whisper.load_model(model_name)

logging.info("Bot started. Wait for voice messages...")
logging.info(f"Used Model: {model_name}")

# Prüfe ob TELEGRAM_SESSION gesetzt ist
if not api_session:
    logging.error("TELEGRAM_SESSION is not set.")
    logging.error("Please set TELEGRAM_SESSION with docker compose run -it app python3 /app/generate_session.py")
    exit()

client = TelegramClient(StringSession(api_session), api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    if event.message.voice:
        logging.info(f"Voicemessage received: {event.message.id}")
        file_path = f"sprachnachricht_{event.message.id}.oga"
        await client.download_media(event.message, file_path)
        try:
            result = model.transcribe(file_path)
            text = result["text"]
            for i in range(0, len(text), 4096):
                await event.reply("Autotranscription:" + text[i : i + 4096])
        except Exception as e:
            await event.reply("Fehler bei der Transkription.")
        finally:
            os.remove(file_path)  # Bereinigung  

client.start()
client.run_until_disconnected()

from telethon import TelegramClient, events
from telethon.sessions import StringSession
import whisper
import os
import logging

logging.basicConfig(level=logging.INFO)

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
api_session = os.getenv("TELEGRAM_SESSION")
telegram_user_id = os.getenv("TELEGRAM_USER_ID")
model_name = os.getenv("WHISPER_MODEL", "medium")
blocked_list = os.getenv("BLOCKED_USERS_CHANNELS", "")
model = whisper.load_model(model_name)

logging.info("Bot started. Wait for voice messages...")
logging.info(f"Used Model: {model_name}")

# Prüfe ob TELEGRAM_SESSION gesetzt ist
if not api_session:
    logging.error("TELEGRAM_SESSION is not set.")
    logging.error("Please set TELEGRAM_SESSION with docker compose run -it app python3 /app/generate_session.py")
    exit()
    
# Prüfe ob TELEGRAM_USER_ID gesetzt ist
if not telegram_user_id:
    logging.error("TELEGRAM_USER_ID is not set.")
    exit()

# Konvertiere TELEGRAM_USER_ID zu int
try:
    telegram_user_id = int(telegram_user_id)
except ValueError:
    logging.error("TELEGRAM_USER_ID must be an integer.")
    exit()

client = TelegramClient(StringSession(api_session), api_id, api_hash)

blocked_users_and_channels = set(map(int, blocked_list.split(','))) if blocked_list else set()

@client.on(events.NewMessage)
async def handler(event):
    sender = await event.get_sender()
    sender_id = sender.id

    # Überprüfen, ob die Nachricht von dir stammt und der Inhalt "?ID?" ist
    if (sender_id == telegram_user_id or telegram_user_id == 0) and event.raw_text == "?ID?":
        await event.reply(f"My ID: {sender_id}\nChat ID: {event.chat_id}")
        return

    if event.message.voice:
        # Überprüfen, ob der Absender in der deaktivierten Liste ist
        if sender_id in blocked_users_and_channels or event.chat_id in blocked_users_and_channels:
            logging.info(f"Autotranscription disabled for user/channel: {sender_id}")
            return

        logging.info(f"Voicemessage received: {event.message.id}")
        file_path = f"sprachnachricht_{event.message.id}.oga"
        await client.download_media(event.message, file_path)
        try:
            result = model.transcribe(file_path)
            text = result["text"]
            for i in range(0, len(text), 4096):
                await event.reply("Autotranscription:" + text[i : i + 4096])
        except whisper.WhisperException as e:
            logging.error(f"Transcription error: {e}")
            await event.reply("Fehler bei der Transkription.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            await event.reply("Ein unerwarteter Fehler ist aufgetreten.")
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)  # Bereinigung  

client.start()
client.run_until_disconnected()

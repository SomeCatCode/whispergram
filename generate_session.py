from telethon import TelegramClient
from telethon.sessions import StringSession
import os

api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print("Your session string:", session_string)
    print("Please set the TELEGRAM_SESSION environment variable to this value.")

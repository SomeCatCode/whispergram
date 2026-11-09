import os
import sys

from telethon import TelegramClient
from telethon.sessions import StringSession

api_id = os.getenv("TELEGRAM_API_ID", "").strip()
api_hash = os.getenv("TELEGRAM_API_HASH", "").strip()

if not api_id or not api_hash:
    print("TELEGRAM_API_ID and TELEGRAM_API_HASH must be set.")
    sys.exit(1)

try:
    api_id = int(api_id)
except ValueError:
    print("TELEGRAM_API_ID must be an integer.")
    sys.exit(1)

with TelegramClient(StringSession(), api_id, api_hash) as client:
    session_string = client.session.save()
    print("Your session string:", session_string)
    print("Please set the TELEGRAM_SESSION environment variable to this value.")

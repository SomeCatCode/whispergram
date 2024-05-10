telethon
# Whispergram

This Docker container project is used to transcribe voice messages from Telegram chats locally with the help of OpenAI's Whisper and automatically post the text transcriptions in the corresponding Telegram chat.
Ideal for anyone who is annoyed by the flood of voice messages.

## Prerequisites
- Docker + Docker Compose
- Telegram API ID and Hash -> ([text](https://core.telegram.org/api/obtaining_api_id))

## Fast Start
```ps
# Clone Repository
git clone https://github.com/SomeCatCode/whispergram.git whispergram

# change into the dir
cd whispergram

# copy env file and change WHISPER_MODEL, TELEGRAM_API_ID and TELEGRAM_API_HASH
cp .env.sample .env
nano .env

# Generate TELEGRAM_SESSION and add them to env file
docker compose run -it app python3 /app/generate_session.py
nano .env

# start the container - all done
docker compose up -d
```
Ersetze dein_bot_token und deine_chat_id durch deine tatsächlichen Telegram-API-Zugangsdaten.

## Functionality
The container listens for new voice messages in a specified Telegram chat. Each received voice message is transcribed using Whisper, and the resulting text transcription is automatically posted as a reply in the same chat.

## License
This project is licensed under the MIT licence. Details can be found in the LICENSE file.
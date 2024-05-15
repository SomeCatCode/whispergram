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

## Functionality
The container listens for new voice messages in a specified Telegram chat. Each received voice message is transcribed using Whisper, and the resulting text transcription is automatically posted as a reply in the same chat.

## How can I get my Telegram ID
If TELEGRAM_USER_ID is set to 0, you can write "?ID?" (without the quotes) in any room. and you get your own ID + that of the room/chat-partners.
!! Attention as long as TELEGRAM_USER_ID is set to 0 this is triggered for every person who writes "?ID?"!! 
After TELEGRAM_USER_ID has been set to your own ID, the command is only triggered for yourself

## How to Exclude Channel
"?ID?" (without the quotes) in a room. Then write the received room/user ID under the variable BLOCKED_USERS_CHANNELS. Multiple ids are separated with ,
Note: Users have a positive ID and chat rooms have a negative one

## License
This project is licensed under the MIT licence. Details can be found in the LICENSE file.

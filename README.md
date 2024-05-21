# Whispergram

Whispergram is a Docker container project that transcribes voice messages from Telegram chats locally with the help of OpenAI's Whisper and automatically posts the text transcriptions in the corresponding Telegram chat. Ideal for anyone who is annoyed by the flood of voice messages.

## Prerequisites
- Docker + Docker Compose
- Telegram API ID and Hash -> ([Instruction of obtaining the credentials](https://core.telegram.org/api/obtaining_api_id))

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
The container listens for new voice messages in a specified Telegram chat. Each received voice message is transcribed with Whisper, and the resulting text transcription is automatically posted as a reply in the same chat.

## How do I get my Telegram ID?
If TELEGRAM_USER_ID is set to 0, you can write "?ID?" (without quotes) in each room. You will then receive your own ID and that of the room/chat partner.
!! Attention: As long as TELEGRAM_USER_ID is set to 0, this command is triggered for every person who writes "?ID?". As soon as TELEGRAM_USER_ID is set to your own ID, the command is only triggered for yourself.

## How to exclude channels and users
Write "?ID?" (without quotes) in a room. Then write the room/user ID received under the variable BLOCKED_USERS_CHANNELS. Multiple IDs are separated by commas.
Note: Users have a positive ID and chat rooms a negative one.

## Update
```ps
# change into the dir
cd whispergram

# pull 
git pull origin main

# start with build flag
docker compose up -d --build
```

## License
This project is licensed under the MIT licence. Details can be found in the LICENSE file.

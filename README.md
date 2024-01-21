# TLDL (Too Long; Didn't Listen)

Originally, **TLDL** is a simple Telegram bot for audio files transcribing. It makes OpenAI Whisper API calls sending the transcribed audio back. 

Lately, I added Dall-e 3 and GPT-3.5/GPT-4 API calls.

The project is ready to local execution, as long as you create a ```.env``` file where you place your own keys for Telegram and OpenAI services. (This includes previously having a created Telegram bot through @BotFather)

## Usage

TLDL bot reacts to commands written on the actual messages you send to it. You must send a slash command like the following to get the response from each endpoint:

- ```/gpt3```: Sends your prompt to ´gpt-3.5-turbo´ model.
- ```/gpt4```: Sends your prompt to ´gpt-4´ model.
- ```/turbo```: Sends your prompt to ´gpt-4-1106-preview´ model.
- ```/dalle```: Sends your prompt to ´dall-e-3´ model.

import os
import numpy as np
import pyshorteners
from util import getChatCompletion, getBasePrompt, getDalle3Img
from dotenv import load_dotenv
from openai import OpenAI
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

load_dotenv(dotenv_path)

TOKEN = os.getenv('TOKEN')
BOT_USERNAME = os.getenv('BOT_USERNAME')
OPENAI_SECRET = os.getenv('OPENAI_SECRET')

client = OpenAI(api_key=OPENAI_SECRET)

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! Send me audios to transcribe and sumarize, or ask me anything for GPT to respond!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I am ready to process your audios! Send some to me"
    )

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command!")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

# Responses
def handle_response(text: str, model: str) -> str:
    prompt: getBasePrompt(text)

    print('Querying ' + model + '...')

    match model:
        case 'dall-e-3':
            img_link = getDalle3Img(client, prompt, pyshorteners)
            return img_link
        case _:
            assistant_content = 'You are a helpful assistant that keeps short and explicative answer when queried.'
            response = getChatCompletion(client, prompt, model, assistant_content)
            return response
        
    #print("============" + str(response) + "==============")

async def handle_voice_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print('handle_voice_response() - Starting')
        
        processing_message = await update.message.reply_text('Procesando el audio...')

        # Obtén el objeto de audio
        voice_file = update.message.voice

        print('handle_voice_response() - Voice file received: ' + str(voice_file))

        # Descarga el archivo de audio
        voice_file = await context.bot.getFile(voice_file.file_id)
        voice_file_path = await voice_file.download_to_drive('voice.mp3')
        print('handle_voice_response() - Voice file path: ' + str(voice_file_path))

        print('handle_voice_response() - Querying whisper...')
        with open(voice_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )

        print('handle_voice_response() - Transcript object' + str(transcript))

        print(f'handle_voice_response() - The text in audio: \n {transcript.text}')

        # Elimina el archivo de audio si ya no lo necesitas
        os.remove(voice_file_path)



        await update.message.reply_text(transcript.text)
    except Exception as e:
        print(f'Error handling audio: {e}')
        await update.message.reply_text('An error occurred while processing the audio 😰')

async def handle_audio_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print('handle_audio_response() - Starting')
        
        # Obtén el objeto de audio
        audio_file = update.message.voice

        print('handle_audio_response() - Audio file received: ' + str(audio_file))

        # Descarga el archivo de audio
        audio_file = await context.bot.getFile(audio_file.file_id)
        audio_file_path = await audio_file.download('audio.mp3')

        print('Audio file path: ' + str(audio_file_path))

        print('handle_audio_response() - Querying whisper')

        #model = whisper.load_model("base")
        #result = model.transcribe(np.array(audio_file_path))
        #sprint(f' The text in video: \n {result["text"]}')

        # Elimina el archivo de audio si ya no lo necesitas
        os.remove(audio_file_path)
        #await update.message.reply_text(result["text"])
    except Exception as e:
        print(f'Error handling audio: {e}')
        await update.message.reply_text('An error occurred while processing the audio 😰')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    model='gpt-3.5-turbo'

    print(f'User {update.message.chat.id} in {message_type}: "{text}"')

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text, model)
        else:
            return
    else:
        if '/gpt3' in text:
            model='gpt-3.5-turbo'
            response: str = handle_response(text, model)
        elif '/gpt4' in text:
            model='gpt-4'
            response: str = handle_response(text, model)
        elif '/turbo' in text:
            model='gpt-4-1106-preview'
            response: str = handle_response(text, model)
        elif '/dalle' in text:
            model='dall-e-3'
            response: str = handle_response(text, model)
        else:
            model='none'
            response: str = handle_response(text, model)
            

    print("Bot:", response)
    await update.message.reply_text(response)


if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    print('Setting commands...')
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))

    # Messages
    print('Setting TEXT and AUDIO MessageHandlers...')
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice_response))
    app.add_handler(MessageHandler(filters.AUDIO, handle_audio_response))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print("Polling...")
    app.run_polling(poll_interval=3)

"""
    openai.api_key = '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'

    response = openai.Completion.create(
      engine="",
      prompt=processed,
      max_tokens=60
    )

    return response.choices[0].text.strip()
"""

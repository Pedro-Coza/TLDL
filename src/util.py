def getChatCompletion(client, prompt, model, assistant_content):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "assistant",
                "content": assistant_content,
            },
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
        max_tokens=500,
    )

    response = chat_completion.choices[0].message.content
    return response

def getBasePrompt(text):
    return text.lower()

def getDalle3Img(client, prompt, pyshorteners):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    shorteners = pyshorteners.Shortener()
    shortlink = shorteners.tinyurl.short(image_url)
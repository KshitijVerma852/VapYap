import os
import openai


client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

# Create a chat completion
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Write me an essay",
        }
    ],
    model="gpt-3.5-turbo",
)

print(response.choices[0].message.content)

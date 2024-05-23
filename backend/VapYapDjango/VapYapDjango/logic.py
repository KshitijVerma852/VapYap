import os
import openai
from django.http import JsonResponse, HttpRequest

client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


def makeAPIRequestFreshSystem(*args):
    chatgptData = {
        "session": {
            "chat_history": []
        }
    }
    for message in args:
        chatgptData["session"]['chat_history'].append(
            {"role": "system", "content": message})
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chatgptData["session"]['chat_history'],
        max_tokens=4096
    )
    ai_response = response.choices[0].message.content
    return ai_response


def makeAPIRequestFreshSystemTurbo(*args):
    chatgptData = {
        "session": {
            "chat_history": []
        }
    }
    for message in args:
        chatgptData["session"]['chat_history'].append(
            {"role": "system", "content": message})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chatgptData["session"]['chat_history']
    )
    ai_response = response.choices[0].message.content
    return ai_response

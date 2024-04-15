import os
import openai
from django.http import JsonResponse, HttpRequest

client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)


def makeAPIRequestFreshSystem(systemMessage, user_message):
    chatgptData = {
        "session": {
            "chat_history": []
        }
    }
    chatgptData["session"]['chat_history'].append({"role": "system", "content": systemMessage})
    chatgptData["session"]['chat_history'].append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chatgptData["session"]['chat_history']
    )
    ai_response = response.choices[0].message.content
    return ai_response


def makeAPIRequestFresh(user_message, chatgptData):
    chatgptData["session"]['chat_history'].append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-3-turbo",
        messages=chatgptData["session"]['chat_history']
    )
    ai_response = response.choices[0].message.content
    return ai_response

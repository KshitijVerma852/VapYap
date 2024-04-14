import os
import openai
from django.http import JsonResponse, HttpRequest


client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)





def returnJSONObject(request):

    system_message = "Please speak to me in Spanish only"
    user_message = "Write a poem"
    ai_response = makeAPIRequestFreshSystem(system_message, user_message, request)



    return JsonResponse({ ai_response})




def makeAPIRequestFreshSystem(systemMessage, user_message, request):
    request.session['chat_history'] = []
    request.session['chat_history'].append({"role": "system", "content": systemMessage})
    request.session['chat_history'].append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=request.session['chat_history']
    )
    ai_response = response.choices[0].message.content
    request.session['chat_history'].append({"role": "system", "content": ai_response})
    request.session.modified = True
    return ai_response


def makeAPIRequestFresh(user_message, request):
    request.session['chat_history'] = []
    request.session['chat_history'].append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-3-turbo",
        messages=request.session['chat_history']
    )
    ai_response = response.choices[0].message.content
    request.session['chat_history'].append({"role": "system", "content": ai_response})
    request.session.modified = True
    return ai_response



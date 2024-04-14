import os
import openai
from django.http import JsonResponse, HttpRequest

client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)



def returnJSONObject(request: HttpRequest):
    user_message = "Write a poem"
    ai_response = makeAPIRequestFresh(user_message, request)

    return JsonResponse({"ai_response": ai_response})




def makeAPIRequestFresh(user_message, request):
    request.session['chat_history'] = []
    request.session['chat_history'].append({"role": "user", "content": user_message})
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=request.session['chat_history']
    )
    ai_response = response.choices[0].message.content
    request.session['chat_history'].append({"role": "system", "content": ai_response})
    request.session.modified = True
    return ai_response



import os
import openai
from django.http import JsonResponse, HttpRequest

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

def returnValue(request: HttpRequest):
    if 'chat_history' not in request.session:
        request.session['chat_history'] = []

    user_message = "Make me a poem"
    request.session['chat_history'].append({"role": "user", "content": user_message})



    # Call OpenAI API with the accumulated chat history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=request.session['chat_history']
    )

    # Extract AI's response and save it to chat histrory
    ai_response = response.choices[0].message["content"]
    request.session['chat_history'].append({"role": "system", "content": ai_response})
    request.session.modified = True

    return JsonResponse({"ai_response": ai_response})

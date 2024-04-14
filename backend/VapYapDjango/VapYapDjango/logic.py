import json
import os
import openai
from django.http import *


client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Tell me a joke",
        }
    ],
    model="gpt-3.5-turbo",
)

def returnValue(request):
    #print(response.choices[0].message.content)
    return HttpResponse(json.dumps(response.choices[0].message.content))


#print(response.choices[0].message.content)
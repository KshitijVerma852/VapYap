from django.contrib import admin
from django.urls import path
from .logic import returnValue
import json
import os
import openai


client = openai.OpenAI(
    api_key=os.environ["OPENAI_API_KEY"]
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Write me a story",
        }
    ],
    model="gpt-3.5-turbo",
)


urlpatterns = [
    path("", returnValue),
    path('admin/', admin.site.urls),
]

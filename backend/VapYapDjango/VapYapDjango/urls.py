from django.contrib import admin
from django.urls import path
from .logic import returnValue
import json
import os
import openai


urlpatterns = [
    path("", returnValue),
    path('admin/', admin.site.urls),
]

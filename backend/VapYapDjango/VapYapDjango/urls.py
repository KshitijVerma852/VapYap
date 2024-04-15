from django.contrib import admin
from django.urls import path
from .parsing import returnJSONObject
import json
import os
import openai


urlpatterns = [
    path("", returnJSONObject),
    path('admin/', admin.site.urls),
]

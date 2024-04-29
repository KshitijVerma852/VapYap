from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .parsing import returnJSONObject
import json
import os
import openai

def index(request):
    return render(request, 'index.html', name='index')


urlpatterns = [
    path("", returnJSONObject),
    path('admin/', admin.site.urls),
]

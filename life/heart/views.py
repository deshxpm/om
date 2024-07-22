from django.shortcuts import render, redirect
from .models import *

def index(request):
    return render(request, 'heart/index.html.j2')
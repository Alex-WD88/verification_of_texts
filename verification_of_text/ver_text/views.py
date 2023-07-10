from django.shortcuts import render
from django.http import HttpResponse
from . import models


def index(request):
    return render(request, 'ver_text/index.html')


def about(request):
    return HttpResponse('<h4>about</h4>')

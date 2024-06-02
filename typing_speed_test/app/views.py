from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return HttpResponse("home page")

def type(request):
    return HttpResponse("Type here")

def result(request):
    return HttpResponse("This is result page")



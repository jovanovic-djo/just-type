from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'typing_speed_test/home.html')

def type(request):
    return render(request, 'typing_speed_test/type.html')

def result(request):
    return render(request, 'typing_speed_test/result.html')



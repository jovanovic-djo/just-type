from django.shortcuts import render
from django.http import HttpResponse
import json
from random import randint


def home(request):
    return render(request, 'typing_speed_test/home.html')

def type(request):
    language = request.POST['language']
    words = request.POST['words']

    match language:
        case "eng200":
            json_data = open('/words/english200.json')
            data = json.load(json_data)
            json_data.close()
        case "eng1k":
            json_data = open('/words/english1k.json')
            data = json.load(json_data)
            json_data.close()
        case "ser":
            json_data = open('/words/serbian.json')
            data = json.load(json_data)
            json_data.close()
    
    match words:
        case "10":
            questions = data["words"]
            random_index = randint(0, 9)

    return render(request, 'typing_speed_test/type.html')


def result(request):
    return render(request, 'typing_speed_test/result.html')



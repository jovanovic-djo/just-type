from django.shortcuts import render
from .utils import load_words
import random


def home(request):
    return render(request, 'typing_speed_test/home.html')

def type(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        word_count = int(request.POST.get('words'))

        words = load_words(language)
        random.shuffle(words)

        selected_words = words[:word_count]

        return render(request, 'typing_speed_test/type.html', {'words': selected_words})
    return render(request, 'typing_speed_test/type.html')


def result(request):
    return render(request, 'typing_speed_test/result.html')



from django.shortcuts import render
from .utils import load_words



def index(request):
    return render(request, "typing_speed_test/index.html")


def type(request):
    if request.method == "POST":
        language = request.POST.get("language")
        word_count = int(request.POST.get("words"))
        accent = request.POST.get("accent")
        topic = request.POST.get("topic")
        complexity = request.POST.get("complexity")

        words = load_words(language, accent, topic, complexity, word_count)
        
        return render(request, "typing_speed_test/type.html", {"words": words})
    return render(request, "typing_speed_test/type.html")

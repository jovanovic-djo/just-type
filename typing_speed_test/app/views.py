from django.shortcuts import render
from .utils import load_words


def index(request):
    return render(request, "typing_speed_test/index.html")


def type(request):
    if request.method == "POST":
        language = request.POST.get("language")
        mode_value = int(request.POST.get("mode-value"))
        accent = request.POST.get("accent")
        topic = request.POST.get("topic")
        complexity = request.POST.get("complexity")

        words = load_words(language, accent, topic, complexity, mode_value)

        return render(request, "typing_speed_test/type.html", {"words": words})
    return render(request, "typing_speed_test/type.html")

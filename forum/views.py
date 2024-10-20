from django.shortcuts import render


def show_forum(request):
    return render(request, "forum.html")

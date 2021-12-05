from django.shortcuts import render


def room(request):
    return render(request, "chat/room.html")

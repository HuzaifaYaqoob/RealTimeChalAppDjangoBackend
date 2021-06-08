from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request , 'index.html')


def Inbox(request , room_name):
    return render(request , 'inbox.html' , {'room_name' : room_name})
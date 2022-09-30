from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Chat, Message
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from .forms import SignUpForm 
# Create your views here.


@login_required(login_url='/login/')
def index(request):
    allUsers = User.objects.all
    allChats = Chat.objects.filter(participant1 = request.user.id) | Chat.objects.filter(participant2 = request.user.id)
    if(request.method == "POST"):
        myChat = Chat.objects.get( id = request.POST.get("chatId"))
        new_message = Message.objects.create(text = request.POST["textmessage"], chat = myChat, author = request.user, reciever = request.user)
        serialized_obj = serializers.serialize('json', [new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
   
    return render(request, 'chat/index.html', {'users': allUsers, "chats": allChats})



def message_view(request):
    allUsers = User.objects.all
    allChats = Chat.objects.filter(participant1 = request.user.id) | Chat.objects.filter(participant2 = request.user.id)
    if(request.method == "POST"):
        print("ich werde ausgeführt mit der ChatID: "+ request.POST.get("chatId"))
        text_messages = Message.objects.filter(chat_id=request.POST.get("chatId"))
        return render(request, 'chat/chat.html', {'messages': text_messages, 'users': allUsers, "chats": allChats})
    return render(request, 'chat/chat.html', {'users': allUsers, "chats": allChats})


def login_view(request):
    redirect = "/"
    if(request.method == "POST"):
        user = authenticate(username = request.POST["username"], password = request.POST["password"])
        if user:
            login(request, user)
            return HttpResponseRedirect(redirect)
        else:
            return HTTPResponseBadRedirect(request)
    return render(request, 'auth/login.html')

def sign_up_view(request):
    redirect = "/"
    if request.method == 'POST':
        user = User.objects.create_user(username = request.POST.get("username"),email=request.POST.get("email"),password=request.POST.get("password1"))
        if user is not None:
           user=authenticate(request, username=request.POST.get("username"), password = request.POST.get("password1"))
           login(request, user)
           return HttpResponseRedirect(redirect)
        else:
           return HTTPResponseBadRedirect(request)
    return render(request, 'auth/sign_up.html')

def logout_view(request):
    logout(request)
    return redirect('/login')


def add_chat(request):
    if request.method == 'POST':
        user = User.objects.get(id = request.POST.get("userId"))
        Chat.objects.create(participant1 = request.user, participant2 = user)
        answer = {"im working": "im working"}
    return JsonResponse(answer,safe=False)

def testFunction2():
    print("i am working 2")

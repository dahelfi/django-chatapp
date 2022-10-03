from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Chat, Message
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


@login_required(login_url='/login/')
def index(request):
    allUsers = User.objects.all
    allChats = Chat.objects.filter(participant1 = request.user.id) | Chat.objects.filter(participant2 = request.user.id)
    if request.method == 'POST':
        print("ich werde ausgeführt")
        user = User.objects.get(id = request.POST.get("userId"))
        new_user = Chat.objects.create(participant1 = request.user, participant2 = user)
        serialized_obj = serializers.serialize('json', [new_user, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
   
    return render(request, 'chat/index.html', {'users': allUsers, "chats": allChats})

@login_required(login_url='/login/')
def message_view(request, id):
    print("ich werde ausgeführt mit der chat id: ", id)
    allUsers = User.objects.all
    allChats = Chat.objects.filter(participant1 = request.user.id) | Chat.objects.filter(participant2 = request.user.id)
    text_messages = Message.objects.filter(chat_id=id)
    myChat = Chat.objects.get(id=id)
    if(request.user.id == myChat.participant1.id):
            recieverUser = myChat.participant2
    else:
        recieverUser = myChat.participant1
    if(request.method == "POST"):
       
        text_messages = Message.objects.filter(chat_id=id)
        new_message = Message.objects.create(text = request.POST["textmessage"], chat = myChat, author = request.user, reciever = recieverUser)
        serialized_obj = serializers.serialize('json', [new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)

    return render(request, 'chat/chat.html', {'messages': text_messages,'users': allUsers, "chats": allChats, "recieverUser": recieverUser})



@csrf_exempt
def login_view(request):
    redirect = "/"
    if(request.method == "POST"):
        user = authenticate(username = request.POST["username"], password = request.POST["password"])
        if user:
            login(request, user)
            return HttpResponseRedirect(redirect)
        else:
            return HttpResponseRedirect(request)
    return render(request, 'auth/login.html')



@csrf_exempt
def sign_up_view(request):
    redirect = "/"
    if request.method == 'POST' and (request.POST.get("password1") == request.POST.get("password2")):
        user = User.objects.create_user(username = request.POST.get("username"),email=request.POST.get("email"),password=request.POST.get("password1"))
        if user is not None:
           user=authenticate(request, username=request.POST.get("username"), password = request.POST.get("password1"))
           login(request, user)
           return HttpResponseRedirect(redirect)
        else:
           return HttpResponseRedirect(request)
    return render(request, 'auth/sign_up.html')

def logout_view(request):
    logout(request)
    return redirect('/login')




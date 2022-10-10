from genericpath import exists
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
@csrf_exempt
def index(request):
    """
    This function renders the overview over all functionalities and possibiltes this programm provides and sends all information 
    the frontend need. 
    """
    all_users = User.objects.all()
    all_chats = Chat.objects.filter(participant1 = request.user.id) | Chat.objects.filter(participant2 = request.user.id)
    if request.method == 'POST':
        user = User.objects.get(id = request.POST.get("userId"))
        existing_chat = checkAndPreventDoubles(user, request.user)
        if(existing_chat == None):
            new_chat = Chat.objects.create(participant1 = request.user, participant2 = user)
            serialized_obj = serializers.serialize('json', [new_chat, ])
            return JsonResponse(serialized_obj[1:-1], safe=False)
        else:
            serialized_obj = serializers.serialize('json', [existing_chat])
            return JsonResponse(serialized_obj[1:-1], safe=False)
    return render(request, 'chat/index.html', {'users': all_users, "chats": all_chats})

def checkAndPreventDoubles(participant1, participant2):
    """
    This function checks if a chat kombination of participant 1 and 2 already exists. If a chat exists this function returns 
    the chat and if not that this function returns NONE.
    """
    possibility1 = Chat.objects.filter(participant1 = participant1) and Chat.objects.filter(participant2 = participant2)
    possibility2 = Chat.objects.filter(participant1 = participant2) and Chat.objects.filter(participant2 = participant1)
    if(possibility1):
        possibility = list(possibility1)
        return possibility[0]
    elif(possibility2):
        possibility2 = list(possibility2)
        return possibility2[0]
    return None

@login_required(login_url='/login/')
@csrf_exempt
def message_view(request, id):
    """
    This function checks render the chat.html view and calculates all information that are needed in the frontend. If a
    post request reach this endpoint a new message will be created and sended to the frontend. 
    """
    all_users = User.objects.all
    all_chats = Chat.objects.filter(participant1 = request.user.id) | Chat.objects.filter(participant2 = request.user.id)
    text_messages = Message.objects.filter(chat_id=id)
    my_chat = Chat.objects.get(id=id)
    if(request.user.id == my_chat.participant1.id):
        reciever_user = my_chat.participant2
    else:
        reciever_user = my_chat.participant1
    if(request.method == "POST"):
        text_messages = Message.objects.filter(chat_id=id)
        new_message = Message.objects.create(text = request.POST["textmessage"], chat = my_chat, author = request.user, reciever = reciever_user)
        serialized_obj = serializers.serialize('json', [new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    return render(request, 'chat/chat.html', {'messages': text_messages,'users': all_users, "chats": all_chats, "recieverUser": reciever_user, "chatId": id})

@csrf_exempt
def login_view(request):
    """
    This function renders the login page and manages the incoming requests depending of the right or wrong credentials 
    """
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
    """
    This function renders the register page and provides the opportunity to create a new user
    """
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
    """
    This function provides the opportunity to end a session and logout
    """
    logout(request)
    return redirect('/login')




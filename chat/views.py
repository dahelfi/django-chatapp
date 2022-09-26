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
    if(request.method == "POST"):
        print("Recieved Data" + request.POST["textmessage"])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text = request.POST["textmessage"], chat = myChat, author = request.user, reciever = request.user )
        serialized_obj = serializers.serialize('json', [new_message, ])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    textMessages = Message.objects.filter(chat__id=1)
    allUsers = User.objects.all
    return render(request, 'chat/index.html', {'messages': textMessages, 'users': allUsers})

def login_view(request):
    redirect = request.GET.get('next')
    if(request.method == "POST"):
        user = authenticate(username = request.POST["username"], password = request.POST["password"])
        if user:
            login(request, user)
            print("request: ", request.POST.get('redirect'))
            HttpResponseRedirect(request.POST.get('redirect'))
            answer = {"stopLoadingAnimation": "true"}
            #serialized_obj = serializers.serialize('json', [stopLoadingAnimation ])
            #print("things gone wrong: ", serialized_obj)
            return JsonResponse( answer, safe=False)
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect} )
    return render(request, 'auth/login.html', {'redirect': redirect})

def sign_up_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password1")
        print("hier dein username: "+ username)
        print("hier dein passwort: "+ password)
        user = User.objects.create_user(username = username,
                                  email=email,
                                  password=password)
        answer = {"stopLoadingAnimation": "true"}
        print("ich werde ausgeführt")
        user=authenticate(request, username=username, password = password)
        if user is not None:
            login(request, user)
        return JsonResponse( answer, safe=False)
       
    return render(request, 'auth/sign_up.html')

def logout_view(request):
    logout(request)
    return redirect('login')

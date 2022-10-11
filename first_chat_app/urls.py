"""first_chat_app URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from first_chat_app import  settings 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static

from chat.views import index, login_view, sign_up_view, logout_view, message_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name=""),
    path("chat/<int:id>/", message_view , name="chat"),
    path("login/", login_view),
    path("sign_up/", sign_up_view, name="sign_up"),
    path("logout/", logout_view, name="logout"),
    static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
]
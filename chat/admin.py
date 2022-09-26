from django.contrib import admin
from chat.models import Message, Chat


class MessageAdmin(admin.ModelAdmin):
    fields = ("chat", "text", "created_at", "author", "reciever")
    list_display = ("text", "created_at", "author", "reciever")
    search_fields = ("hallo",)


# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)

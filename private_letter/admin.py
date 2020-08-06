from django.contrib import admin
from .models import Chat,PrivateLetter

# Register your models here.

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
	list_display = ('id','user1','user2')

@admin.register(PrivateLetter)
class privateLetterAdmin(admin.ModelAdmin):
	list_display = ('id','sender','time','chat')
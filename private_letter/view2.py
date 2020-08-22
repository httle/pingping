from django.shortcuts import render,get_object_or_404
from django.db.models.signals import post_save
from notifications.signals import notify
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.models import User
from user.models import FriendsSystem
from .models import Chat,PrivateLetter




def privateLetter2json(chatMessage,user):

	return{
		'time':chatMessage.time,
		'text':chatMessage.text,
		'sender':chatMessage.sender.username,
		'img':str(chatMessage.image),
		'ifsender':1 if user==chatMessage.sender else 0
	}



def startChat(request):
	chatobjpk = request.GET.get('chatobjid','')
	chatobj = User.objects.filter(pk = chatobjpk)
	if chatobj:
		chat = Chat.objects.filter(Q(user1 = request.user) | Q(user2 = request.user)).filter(Q(user1 = chatobj[0]) | Q(user2 = chatobj[0]))
		if chat:
			data = []
			ifhave = 1
			chatpk = chat[0].pk
			privateLetters = PrivateLetter.objects.filter(chat = chat[0])
			for i in privateLetters:
				strs = privateLetter2json(i,request.user)
				data.append(strs)
			return JsonResponse({
					"status":1,
					"data":data,
					"id":chatpk,
					"ifhave":ifhave,
					"objname":chatobj[0].username,
				})
		else:
			ifhave = 0
			chat = Chat()
			chat.user1 = request.user
			chat.user2 = chatobj[0]
			chat.save()
			return JsonResponse({
					"status":1,
					"ifhave":ifhave,
					"id":chat.pk,
					"objname":chatobj[0].username,
				})
	return JsonResponse({
			"status":0
		})

def appStartChat(request):
	username = request.GET.get('username','')
	chatername = request.GET.get('chatername','')
	print(username,chatername)
	user = User.objects.get(username = username)
	chater = User.objects.get(username = chatername)
	chat = Chat.objects.filter(Q(user1 = user) | Q(user2 = user)).filter(Q(user1 = chater) | Q(user2 = chater))
	if chat:
		return JsonResponse({
				"pk":chat[0].pk
			})
	else:
		startchat = Chat()
		startchat.user1 = user
		startchat.user2 = chater
		startchat.unread = 0
		startchat.save()
		return JsonResponse({
				"pk":startchat.pk
			})

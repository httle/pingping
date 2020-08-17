import string
import random
import time 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from notifications.signals import notify
from notifications.models import Notification
from django.db.models import Q
from django.contrib import auth
from django.urls import reverse
from django.http import JsonResponse
from .models import FriendsSystem

def sendFriendNotify(request):
	pk = request.GET.get("id","0")
	friend = User.objects.get(pk = pk)
	friendMake = FriendsSystem.objects.filter(Q(user1 = request.user) | Q(user2 = request.user)).filter(Q(user1 = friend) | Q(user2 = friend)).filter(ifprocess=0)
	if (friendMake):
		ifsend = 1
		ifsuccess = 0
	else:
		makeFriend = FriendsSystem()
		makeFriend.user1 = request.user
		makeFriend.user2 = friend
		makeFriend.agreesender = request.user
		makeFriend.agreereceiver = friend
		makeFriend.agree = 0
		makeFriend.save()
		ifsuccess = 1
		ifsend = 0
		verb = "您收到一条好友请求"
		description = request.user.username+"向你发起了好友请求"
		url = "http://47.93.251.168:8000/privaletter/"
		notify.send(request.user,recipient = friend,verb = verb,action_object = makeFriend,url = url,description = description)
	return JsonResponse({
			"ifsuccess":ifsuccess,
			"ifsend":ifsend
		})

def friendlist2json(friendNotify):
	return{
		"sender":friendNotify.agreesender.username,
		"pk":friendNotify.pk
	}

def friendNotifyList(request):
	a = FriendsSystem()
	contentType = ContentType.objects.get_for_model(a)
	friendNotifications = Notification.objects.filter(recipient = request.user,action_object_content_type = contentType,unread = False)
	for i in friendNotifications:
		i.delete()
	friendNotifys = FriendsSystem.objects.filter(agreereceiver = request.user,ifprocess=False)
	data = []
	for friendNotify in friendNotifys:
		string = friendlist2json(friendNotify)
		data.append(string)
	return JsonResponse({
			"data":data
		})

def friendProcess(request):
	mode = int(request.GET.get('mode',''))
	pk = int(request.GET.get('id',-1))
	if(pk!=-1):
		friendMake = FriendsSystem.objects.get(pk=pk)
	status = 0
	if(mode==0):
		friendMake.ifprocess = True
		friendMake.agree = 2
		friendMake.delete()
		verb = "您收到一条好友消息"
		description = friendMake.agreereceiver.username+"拒绝了你的好友请求"
		notify.send(recipient = friendMake.agreesender,sender = friendMake.agreereceiver,verb = verb,description = description,url =url)
		status = 1
	elif(mode==1):
		friendMake.ifprocess = True
		friendMake.agree = 1
		friendMake.save()
		status = 1
		verb = "您收到一条好友消息"
		description = friendMake.agreereceiver.username+"接受了你的好友请求"
		notify.send(recipient = friendMake.agreesender,sender = friendMake.agreereceiver,verb = verb,description = description,url =url)
	return JsonResponse({
			"status":status,
			"friend":friendMake.agreesender.username,
		})


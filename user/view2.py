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
from private_letter.models import Chat


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
	url = "http://47.93.251.168:8000/privaletter/"
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

def appfriendList2json(friend,user):
	chat = Chat.objects.filter((Q(user1 = friend.user1) | Q(user2 = friend.user1)),(Q(user1 = friend.user2) | Q(user2 = friend.user2)))
	if chat:
		chatpk = chat[0].pk
		return {
			'friend':chat[0].user1.username if chat[0].user2==user else chat[0].user2.username,
			'chatpk':chatpk,
		}
	else:
		chat = Chat()
		chat.user1 = friend.user1
		chat.user2 = friend.user2
		chat.unread = 0
		chat.save()
		chatpk = chat.pk
		return {
			'friend':chat.user1.username if chat.user2==user else chat.user2.username,
			'chatpk':chatpk,
		}


def appFriendList(request):
	username = request.GET.get('username','')
	user = User.objects.get(username = username)
	friends = FriendsSystem.objects.filter((Q(user1 = user) | Q(user2 = user)),agree = 1)
	data = []
	for friend in friends:
		string = appfriendList2json(friend,user)
		data.append(string)
	return JsonResponse({
			'data':data,
		})


def appFriendProcess2json(process):
	return {
		'agreesender':process.agreesender.username,
		'pk':process.pk,
	}


def appFriendProcessList(request):
	username = request.GET.get('username','')
	user = User.objects.get(username = username)
	friendProcessList = FriendsSystem.objects.filter(agreereceiver = user,ifprocess = False)
	data = []
	for process in friendProcessList:
		strs = appFriendProcess2json(process)
		data.append(strs)

	return JsonResponse({
			'data':data
		})

def appFriendProcess(request):
	pk = request.GET.get('pk',-1)
	mode = request.GET.get('mode','0')
	print("pk:"+pk+"and mode:"+mode)
	if(pk!=-1):
		friendMake = FriendsSystem.objects.get(pk=pk)
	if(int(mode)==0):
		friendMake.ifprocess = True
		friendMake.agree = 2
		friendMake.delete()
		print("frienddelete")
	else:
		friendMake.ifprocess = True
		friendMake.agree = 1
		friendMake.save()
		print("friendMake")
	return JsonResponse({
			"status":0,
		})


def appMakeFriend(request):
	username = request.GET.get('username','')
	friendname = request.GET.get('friendname','')
	user = User.objects.get(username = username)
	friend = User.objects.get(username = friendname)
	status = 0
	print(username,friendname)
	friendSystem = FriendsSystem.objects.filter(Q(user1 = user) | Q(user2 = user)).filter(Q(user1 = friend) | Q(user2 = friend))
	if(friendSystem):
		if(friendSystem[0].ifprocess==0):
			status = 1
		else:
			status = 0
	else:
		makeFriend = FriendsSystem()
		makeFriend.user1 = user
		makeFriend.user2 = friend
		makeFriend.agreesender = user
		makeFriend.agreereceiver = friend
		makeFriend.save()
		status = 2

	return JsonResponse({
			"status":status,
			# "text":"success",
		})
	# return JsonResponse({"data":{
 #        'statue':status,
 #        'text':"success"
 #    }},safe=False)

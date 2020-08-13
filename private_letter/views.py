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

# Create your views here.


def privateLetter(request):
	context = {}
	# mode = request.GET.get("mode",'0')
	# print("mode="+mode)
	context["iffromWeb"] = 0
	# if(str(mode) == '1'):
	# 	print("inter")
	# 	context["iffromWeb"] = 1
	# 	chater = request.GET.get("chater","")
	# 	chater = User.objects.get(username = chater)
	# 	ifchat = Chat.objects.filter(Q(user1 = request.user) | Q(user2 = request.user)).filter(Q(user1 = chater) | Q(user2 = chater))
	# 	if(ifchat):
	# 		privateLetters = PrivateLetter.objects.filter(chat = ifchat[0])
	# 		context["privateLetters"] = privateLetters
	# 		context["selectedpk"] = ifchat[0].pk
	# 		print("havechat")
	# 	else:
	# 		toChater = Chat()
	# 		toChater.user1 = request.user
	# 		toChater.user2 = chater
	# 		toChater.unread = 0
	# 		toChater.save()
	# 		context["selectedpk"] = toChater.pk
	# 		print("nothaveChat")
	# else:
	# 	print("notenter")



	chats = Chat.objects.filter(Q(user1 = request.user) | Q(user2 = request.user))
	friends = FriendsSystem.objects.filter((Q(user1 = request.user) | Q(user2 = request.user)),agree = 1)
	
	context["chats"] = chats
	context["friends"] = friends
	for chat in chats:
		contentType = ContentType.objects.get_for_model(chat)
		notification = Notification.objects.filter(recipient = request.user,unread = True,
			action_object_content_type = contentType,action_object_object_id = chat.pk)
		chat.unread = notification.count()
		# print(notification.count())
	# for i in friends:
	# 	print(i.user1.username)
	return render(request, 'privateLetter/test2.html',context)

def chatMessage(request):
	chatid = request.GET.get('id')
	print(chatid)
	print(request.user.username)
	chat = 	Chat.objects.get(pk = chatid)
	chat.unread = 0
	privateLetters = PrivateLetter.objects.filter(chat = chat)
	contentType = ContentType.objects.get_for_model(chat)
	notification = Notification.objects.filter(recipient = request.user,
		action_object_content_type = contentType,action_object_object_id = chat.pk)
	if(not notification == None):
		print("success")
		notification.unread = False
		notification.delete()
	data = []
	for i in privateLetters:
		strs = privateLetter2json(i,request.user)
		data.append(strs)
	# print(data)
	return JsonResponse({
			'status': "success",
			'chatMessage':data,
			'chatId':chatid,
		})

def privateLetter2json(chatMessage,user):

	return{
		'time':chatMessage.time,
		'text':chatMessage.text,
		'sender':chatMessage.sender.username,
		'img':str(chatMessage.image),
		'ifsender':1 if user==chatMessage.sender else 0
	}


def sendChatMes(request):
	text = request.GET.get('text','')
	print(text)
	chatId = request.GET.get('id','')
	print(chatId)
	name = request.GET.get('name','')
	print(name)
	status = "failed"
	if(name!='' and chatId!='' and text!=''):
		user = User.objects.get(username = name)
		chatMes = PrivateLetter()
		chat = Chat.objects.get(pk = chatId)
		if(chat.user1==user or chat.user2==user):
			chatMes.chat = chat
			chatMes.text = text
			chatMes.sender = user
			chatMes.receiver = chat.user1 if chat.user2==user else chat.user2
			chatMes.save()
			verb = "收到一条消息"
			description = "您收到一条消息"
			notify.send(user,recipient=chatMes.receiver,verb=verb,
				action_object=chatMes.chat,description = description)
			status = "success"

	return JsonResponse({
			'status': status,
		})


def chat2json(chat):
	return {
		'pk':chat.pk,
		'user1':chat.user1.username,
		'user2':chat.user2.username,
		'unread':chat.unreadNum,
	}

def appchat2json(chat,user):
	return {
		'pk':chat.pk,
		'user1':chat.user1.username if chat.user2==user else chat.user2.username,
		'user2':chat.user2.username,
		'unread':chat.unreadNum,
	}

def appChatList(request):
	user = request.GET.get('user','')
	print(user+"send")
	user = get_object_or_404(User,username = user)
	chats = Chat.objects.filter(Q(user1 = user) | Q(user2 = user))
	data = []
	for chat in chats:
		string = appchat2json(chat,user)
		data.append(string)

	return JsonResponse({
			"data":data
		},safe = False)


def appDetailChat(request):
	pk = request.GET.get('pk',0)
	username = request.GET.get('user','')
	user = User.objects.get(username = username)
	print(pk+"and"+"username")
	if(pk!=0 and user !=None):
		chat = Chat.objects.get(pk = pk)
		chat.unread = 0
		privateLetters = PrivateLetter.objects.filter(chat = chat)
		contentType = ContentType.objects.get_for_model(chat)
		notification = Notification.objects.filter(recipient = user,
			action_object_content_type = contentType,
			action_object_object_id = chat.pk)
		if(not notification == None):
			print("success")
			notification.unread = False
			notification.delete()
		data = []
		for i in privateLetters:
			str = privateLetter2json(i,user)
			data.append(str)
		print(data)
		return JsonResponse({
				'status': "success",
				'chatMessage':data,
			})
	else:
		return JsonResponse({
				'status': "failed",
			})


def appChatSend(request):
	user = request.POST.get('user','')

	reply = request.POST.get('reply','')
	pk = request.POST.get('pk','')
	status = 0
	print(user+"and"+reply+"and"+pk)
	user = User.objects.get(username = user)
	chat = Chat.objects.get(pk = pk)
	if(user!='' and user !=None and chat!=None):
		chatMes = PrivateLetter()
		chatMes.chat = chat
		chatMes.text = reply
		chatMes.sender = user
		chatMes.receiver = chat.user1 if user==chat.user2 else chat.user2
		chatMes.save()
		privateLetters = PrivateLetter.objects.filter(chat = chat)
		status = 1
		data = []
		for i in privateLetters:
			str = privateLetter2json(i,user)
			data.append(str)
		return JsonResponse({
				'status': "success",
				'chatMessage':data,
			})
	return JsonResponse({"res":{
	        'statue':status,
	        'text':"failed"
	    },"data":data},safe=False)



def webNotifyJson(chat):
	return {
		'unreadnum':chat.unread,
		'pk':chat.pk,
	}

def webChatNotify(request):
	chats = Chat.objects.filter(Q(user1 = request.user) | Q(user2 = request.user))
	chatid = request.GET.get('id','')
	# print(chatid)
	text = []
	data = []
	for chat in chats:
		contentType = ContentType.objects.get_for_model(chat)
		notification = Notification.objects.filter(recipient = request.user,unread = True,
			action_object_content_type = contentType,action_object_object_id = chat.pk)
		chat.unread = notification.count()
		if(str(chat.pk)==chatid):
			privateLetters = PrivateLetter.objects.filter(chat = chat)
			# print("failed")
			# print(chat.unread)
			for i in privateLetters[(len(privateLetters)-chat.unread):len(privateLetters)]:
				# print("success")
				text.append({'text':i.text})
				# print(i.text)
			for i in notification:
				i.unread = False
				i.save()
			chat.unread = 0
		string = webNotifyJson(chat)
		data.append(string)
	return JsonResponse({
		'text':text,
		'data':data,
	})

	

	


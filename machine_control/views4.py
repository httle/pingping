from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import MachineControl,CoachSystem,ApplySystem
from user.models import FriendsSystem
from django.db.models import Count,Q
import json

def user2Json(searchUser,user):
	status = 0
	coachSystem = CoachSystem.objects.filter(Q(user = searchUser)| Q(user = user)).filter(Q(coach = searchUser) | Q(coach = user))
	ifapply = ApplySystem.objects.filter(Q(applyCoach = user) | Q(applyCoach = searchUser)).filter(Q(applyLearner = user) | Q(applyLearner = searchUser)).filter(ifprocess = False)
	if coachSystem:
		if(coachSystem[0].user == user):
			status = 1
		else:
			status = 2
	elif ifapply:
		status = 3
	else:
		status = 0
	return{
		'user':searchUser.username,
		'pk':searchUser.pk,
		'status':status,
	}

def userSearch(request):
	username = request.GET.get('user','')
	user = User.objects.get(username = username)
	kw = request.GET.get('kw','')
	print(kw)
	if (kw):
		search_word = kw.strip()
		condition = None
		for word in search_word:
			if condition is None:
				condition = Q(username__icontains = word)
			else:
				condition = condition | Q(username__icontains = word)
		if condition is not None:
			users = User.objects.filter(condition).exclude(username = username)
			data = []
			for i in users:
				strs = user2Json(i, user)
				data.append(strs)
				# print(data)
	else:
		users = User.objects.exclude(username = username)
		data = []
		for i in users:
			strs = user2Json(i, user)
			data.append(strs)
		# print(data)
	return JsonResponse({
			'data':data
		})

def applyList2json(apply,user):
	applyer = apply.applyCoach if apply.applyLearner == user else apply.applyLearner
	if(apply.applyCoach == user):
		status=1
	else:
		status=2
	return {
		'applyer': applyer.username,
		'pk':applyer.pk,
		'status':status
	}

def applyList(request):
	username = request.GET.get('username','')
	user = User.objects.get(username = username)
	applyLists = ApplySystem.objects.filter(Q(applyCoach = user)| Q(applyLearner = user)).filter(ifprocess = False)
	data = []
	for i in applyLists:
		strs = applyList2json(i, user)
		data.append(strs)
	return JsonResponse({
			'data':data
		})

def applyProcess(request):
	pk = request.GET.get('pk',0)
	applyer = User.objects.get(pk = pk)
	username = request.GET.get('username','')
	user = User.objects.get(username = username)
	ifaccept = request.GET.get('status',0)
	status = 1
	# print(applyer.username,username,ifaccept)
	applySystem = ApplySystem.objects.filter(Q(applyCoach = user) | Q(applyLearner = user)).filter(Q(applyCoach = applyer) | Q(applyLearner = applyer)).filter(ifprocess = False)
	if applySystem:
		if(int(ifaccept)==1):
			applySystem[0].ifprocess = True
			applySystem[0].status = 1
			applySystem[0].save()
			coachSystem = CoachSystem()
			coachSystem.user = applySystem[0].applyLearner
			coachSystem.coach = applySystem[0].applyCoach
			coachSystem.save()
			friend = FriendsSystem.objects.filter(Q(user1 = user) | Q(user1 = applyer)).filter(Q(user2 = user) | Q(user2 = applyer))
			if(friend):
				friend[0].agree = 1
				friend[0].ifprocess = True
				friend[0].save()
				print("makefriend2")
			else:
				friend = FriendsSystem()
				friend.user1 = applyer
				friend.user2 = user
				friend.agreesender = applyer
				friend.agreereceiver = user
				friend.agree = 1
				friend.ifprocess = True
				friend.save()
				print("makefriend")
			# print("success")
			
		else:
			applySystem[0].ifprocess = True
			applySystem[0].status = 2
			applySystem[0].delete()
			print(ifaccept,"failed")
	else:
		status = 0
	return JsonResponse({
			'status':status
		})

def appApplySend(request):
	username = request.GET.get('username','')
	user = User.objects.get(username = username)
	pk = request.GET.get('pk',0)
	applyObj = User.objects.get(pk = pk)
	applytarget = request.GET.get('status',0)
	print(applytarget)
	status = 0
	applySystem = ApplySystem()
	if(int(applytarget)==1):
		applySystem.applyCoach = applyObj
		applySystem.applyLearner = user
		applySystem.save()
		status = 1
	elif(int(applytarget)==2):
		applySystem.applyCoach = user
		applySystem.applyLearner = applyObj
		applySystem.save()
		status = 1
	return JsonResponse({
			'status':status,
		})


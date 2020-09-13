from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import MachineControl,CoachSystem
import json

def machineUsing(request):
	username = request.POST.get('user','')
	user = User.objects.get(username = username)
	machineNum = request.POST.get('machineNum',0)
	print(username+"and"+machineNum)
	machine = MachineControl.objects.filter(machine_num = int(machineNum))
	if machine:
		machine[0].user = user
		machine[0].ifusing = True
		machine[0].save()
		status = 1
		text = "使用成功"
	else:
		status = 0
		text = "使用失败"
	return JsonResponse({
		"status":status,
		})

def learner2json(learner):
	machine = MachineControl.objects.filter(user = learner.user)
	if machine:
		ifusing = 1
		machine_num = machine[0].machine_num
	else:
		ifusing = 0
		machine_num = 0
	return{
		'learner':learner.user.username,
		'ifusing':ifusing,
		'machine_num':machine_num,
	}

def coacher2json(coach):
	return{
		'coach':coach.coach.username,
	}

def learnerList(request):
	coachname = request.GET.get('coachname','')
	print(coachname)
	coach = User.objects.get(username = coachname)
	learners = CoachSystem.objects.filter(coach = coach)
	data = []
	for i in learners:
		strs = learner2json(i)
		data.append(strs)
	print(data)
	coachs = CoachSystem.objects.filter(user = coach)
	data2 = []
	for i in coachs:
		strs = coacher2json(i)
		data2.append(strs)
	print(data2)
	return JsonResponse({
			'data':data,
			'data2':data2
		})

def coachSet(request):
	print("1231")
	dataJson = request.POST.get('data','')
	data  = json.loads(dataJson)
	for i in data:
		print(i["up"])
		print(i["mid"])
		print(i["bo"])
		print(i["num"])
	print(dataJson+"receive")
	return JsonResponse({
			'data':1
		})
	

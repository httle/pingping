from django.http import JsonResponse
import json
from django.shortcuts import render
# from .my_socket_web import socket_web
import socket
import time
from multiprocessing import Process
from django.contrib.auth.models import User
from .models import Practice,PracticeImg,MachineControl
# Create your views here.
def appControl(request):
    statue = 1
    text = "发送成功"
    username = request.POST.get('username','')
    machineNum = request.POST.get('machineNum',0)
    user = User.objects.get(username = username)
    machine = MachineControl.objects.filter(machine_num = int(machineNum))
    ifcoach = request.POST.get('ifcoach',0)
    print(ifcoach)
    if machine:
        if(machine[0].user == user and machine[0].ifusing==1):
            print("machineUsingSuccess")
        else:
            statue = 0
            text = "操作失败"
            return JsonResponse({"data":{
                    'statue':statue,
                    'text': text,
                }},safe=False)
    else:
        statue = 0
        text = "操作失败"
        return JsonResponse({"data":{
                    'statue':statue,
                    'text': text,
                }},safe=False)


    ifup = request.POST.get('ifup',0)
    upSpeed = request.POST.get('upSpeed',0)
    ifmid = request.POST.get('ifmid',0)
    midSpeed = request.POST.get('midSpeed',0)
    ifbo = request.POST.get('ifbo',0)
    boSpeed = request.POST.get('boSpeed',0)
    ifcon = request.POST.get('ifcon',0)
    ifend = request.POST.get('ifend',1)
    mode = request.POST.get('mode',0)
    sendpractice = request.POST.get('sendpractice',0)
    actionList  = request.POST.get('data','')
    
    print(ifcon)
    print(ifup,upSpeed)
    print(ifmid,midSpeed)
    print(ifbo,boSpeed)
    data={
        'sendpractice':sendpractice,
        'ifend':ifend,
        'mainControl':ifcon,
        'mode':mode,
        'actionList':actionList,
        'data':{
            'ifup':ifup,
            'upSpeed':upSpeed,
            'ifmid':ifmid,
            'midSpeed':midSpeed,
            'ifbo':ifbo,
            'boSpeed':boSpeed,
        }
    }
    data_json = json.dumps(data)
    print(data)
    # try:
    #     socket_web(data_json)
    # except Exception as e:
    #     pass
    socket_web(data_json)

    if(ifup =='' or ifmid=='' or ifbo=='' or
            upSpeed=='' or midSpeed=='' or boSpeed==''):
        statue=0
        text = "发送失败"
        
    return JsonResponse({"data":{
        'statue':statue,
        'text': text,
    }},safe=False)


def socket_web(data_json):
    HOST = '172.29.52.94'
    PORT = 7000
    my_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    my_socket.bind((HOST,PORT))
    my_socket.listen(1)
    conn,addr = my_socket.accept()
    conn.send(data_json.encode())
    time.sleep(3)
    conn.close()
    # try:
    #     mysocket.settimeout(7)
    #     my_socket.bind((HOST,PORT))
    #     my_socket.listen(1)
    #     conn,addr = my_socket.accept()
    #     conn.send(data_json.encode())
    #     time.sleep(3)
    #     conn.close()
    # except Exception as e:
    #     print(e)
    # print("end")

def test(request):
    try:
        a=1/0
    except Exception as e:
        print(e)
    return JsonResponse({"data":{
        'statue':0,
        'text': "出错",
    }},safe=False)

def uploadPracData(request):
    statue = 1
    user_name = request.POST.get('user','')
    prac_num = request.POST.get('practice_num',-1)
    hit_percent = request.POST.get('hit_percent',0.0)
    prac_imgs = request.FILES.getlist('img',None)
    print(user_name)
    print(prac_num)
    print(prac_imgs)
    user = User.objects.get(username = user_name)
    if(user and prac_num!=-1):
        practice = Practice()
        practice.user = user
        practice.practice_num = prac_num
        practice.hit_percent = hit_percent
        practice.save()
        if(prac_imgs):
            for f in prac_imgs:
                prac_img = PracticeImg()
                prac_img.practice = practice
                prac_img.img = f
                prac_img.save()

    else:
        statue = 0
        return JsonResponse({"data":{
            'statue':statue,
            'text':"failed"
        }},safe=False)

    return JsonResponse({"data":{
            'statue':statue,
            'text':"success"
        }},safe=False)
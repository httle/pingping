from django.http import JsonResponse
import json
from django.shortcuts import render
# from .my_socket_web import socket_web
import socket
import time
from multiprocessing import Process
from django.contrib.auth.models import User
from .models import Practice,PracticeImg
# Create your views here.
def appControl(request):
    statue = 1
    text = "发送成功"
    ifup = request.POST.get('ifup','')
    upSpeed = request.POST.get('upSpeed','')
    ifmid = request.POST.get('ifmid','')
    midSpeed = request.POST.get('midSpeed','')
    ifbo = request.POST.get('ifbo','')
    boSpeed = request.POST.get('boSpeed','')
    print(ifup,upSpeed)
    print(ifmid,midSpeed)
    print(ifbo,boSpeed)
    data={
        'mainControl':1,
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
    user = User.objects.get(usrname = user_name)
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
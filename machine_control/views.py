from django.http import JsonResponse
import json
from django.shortcuts import render
# from .my_socket_web import socket_web
import socket
import time
from multiprocessing import Process
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
    # while True:
    #     time.sleep(2)
    #     rec = conn.recv(1024)
    #     msg = rec.decode()
    #     print(msg)
    #     if msg == "end":
    #         break
    time.sleep(1)
    conn.close()
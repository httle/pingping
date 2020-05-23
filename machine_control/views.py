from django.http import JsonResponse
import json
from django.shortcuts import render

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
    # socket_data(data_json)
    print(data)
    if(ifup =='' or ifmid=='' or ifbo=='' or
            upSpeed=='' or midSpeed=='' or boSpeed==''):
        statue=0
        text = "发送失败"

    return JsonResponse({"data":{
        'statue':statue,
        'text': text,
    }},safe=False)

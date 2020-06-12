from django.http import JsonResponse
from django.shortcuts import redirect,render,get_object_or_404
from notifications.models import Notification
from django.urls import reverse
from django.contrib.auth.models import User
from comment.models import Comment
import re



def my_notifications(request):
    context={}
    return render(request, 'my_notifications/my_notifications.html',context)

def my_notification(request,my_notification_pk):
    my_notification = get_object_or_404(Notification,pk=my_notification_pk)
    my_notification.unread = False
    my_notification.save()
    return redirect(my_notification.data['url'])

def my_notification_delete(request):
	notifications = request.user.notifications.read()
	notifications.delete()
	return redirect(reverse('my_notifications'))

def app_notification_change(request):
    user = request.GET.get('user', '')
    user = get_object_or_404(User, username=user)
    mode = request.GET.get('mode','')
    print(mode)
    if(int(mode)==1):
        notifications = user.notifications.unread()
        for i in notifications:
            i.unread = False
            i.save()
            pass
        print("已读")
        return JsonResponse({"data":{
        'statue':1,
        'text': '全部已读',
    }},safe=False)
    elif(int(mode)==2):
        notifications = user.notifications.read()
        notifications.delete()
        print("已删")
        return JsonResponse({"data":{
        'statue':1,
        'text': '全部删除',
    }},safe=False)
    elif(int(mode)==3):
        pk = request.GET.get('object_id',-1)
        pk = (int)(pk)
        print(pk)
        my_notification = get_object_or_404(Notification, pk=pk)
        my_notification.unread = False
        my_notification.save()
        print("success")
        return JsonResponse({"data": {
            'statue': 1,
            'text': '已阅',
        }}, safe=False)
    else:
        return JsonResponse({"data":{
        'statue':0,
        'text': '操作失败',
    }},safe=False)


def app_notification(request):
    user = request.GET.get('user','')
    user = get_object_or_404(User,username = user)
    notifications = user.notifications.all()
    messages = []
    num = 0
    for i in notifications:
        message = message2json(i)
        messages.append(message)
        num+=1
    return JsonResponse({"data":messages},safe=False)

def message2json(message):
    # 数据转化为json
    print(message.action_object.pk)
    comment = Comment.objects.get(pk = message.action_object.pk)
    return{
        'pk':message.pk,
        'actor':message.actor.username,
        'verb':message.verb,
        'description':message.description,
        'time':message.timesince(),
        "unread":message.unread,
        'blog_pk':comment.object_id,
        'root_pk':comment.root.pk if comment.root!=None else 0,

    }
def app_notification_new(request):
    user = request.GET.get('user','')
    user = get_object_or_404(User,username = user)
    notifications = user.notifications.unread()
    num = 0
    for i in notifications.reverse():
        num+=1
    return JsonResponse({
        "statue":1,
        "text":num,
    },safe=False)
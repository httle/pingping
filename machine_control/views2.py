from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count,Q
from django.contrib.contenttypes.models import ContentType
from .models import Practice,PracticeImg
from django.contrib.auth.models import User


def get_practice_list_common_data(request,practice_all_list):
    paginator = Paginator(practice_all_list, settings.EACH_PAGE_NUMBER)  # 每页10篇
    page_num = request.GET.get('page', 1)  # 获取url的页面参数（GET请求)
    page_of_practice = paginator.get_page(page_num)
    page_range = [x for x in range(int(page_num) - 2, int(page_num) + 3) if 0 < x <= paginator.num_pages]  # 用于显示页面的前后两页

    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context = {}
    context['page_of_practice'] = page_of_practice
    context['page_range'] = page_range
    return context


def practice_list(request):
    # 列表页
    user = request.user
    print(user.username)
    practice_all_list = Practice.objects.get(user = user)
    context = get_practice_list_common_data(request, practice_all_list)
    return render(request, 'machine_control/practice_list.html', context)

def practice_detail(request,practice_pk):
    # 具体内容
    practice=get_object_or_404(Practice,pk=practice_pk)
    context={}
    
    context['previous_practice']=Practice.objects.filter(created_time__gt=practice.created_time).last()
    context['next_practice']=Practice.objects.filter(created_time__lt=practice.created_time).first()
    # 这里的__gt和__lt表示大于等于和小于等于，这里用created_time作为标准而不是id是因为当一些博客被删除后，
    # 其id也会占着位置，导致出错，所以用created_time比较好
    context['practice']=practice
    context['imgs'] = PracticeImg.objects.filter(practice = practice)
    for img in context['imgs']:
        print(img.img)
    response = render(request,'machine_control/practice_detail.html',context) #响应
    return response

def pratice2json(practice):
    # 将给app的数据转化为json格式
    imgs = PracticeImg.objects.filter(practice = practice)
    imglist = []
    for img in imgs:
        imglist.append("http://47.93.251.168:8000/media/"+str(img.img))
    return{
        'praticeNum':practice.pk,
        'time':practice.created_time,
        'data':practice.data,
        'hit_percent':practice.hit_percent,
        'practice_num':practice.practice_num,
        'PracticeImg':imglist,
    }


def app_practice(request):
    username = request.GET.get('user','')
    print(username)
    user = User.objects.get(username = username)
    practice_list = Practice.objects.filter(user = user)
    paginator = Paginator(practice_list,settings.EACH_PAGE_NUMBER)
    page_num = request.GET.get('page',1)
    print(page_num)
    page_of_practice = paginator.get_page(page_num)
    data = []

    for practice in page_of_practice:
        str = pratice2json(practice)
        data.append(str)

    return JsonResponse({"total_num":paginator.num_pages,"data":data},safe=False)

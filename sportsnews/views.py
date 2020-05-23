from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import SportsNews
import re
import urllib
# Create your views here.
def sportsNewsList(request):
    # getnews()
    allNews = SportsNews.objects.all().order_by('-created_time')
    paginator = Paginator(allNews,settings.EACH_PAGE_NUMBER)
    page_num = request.GET.get('page',1)
    newsList = paginator.get_page(page_num)
    page_range = [x for x in range(int(page_num) - 2, int(page_num) + 3) if 0 < x <= paginator.num_pages]
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
    context['news_list'] = newsList
    context['page_range'] = page_range
    return render(request,'sportsnews/sportsnews.html',context)

def appSportsNews(request):
    allNews = SportsNews.objects.all().order_by('-created_time')
    paginator = Paginator(allNews,settings.EACH_PAGE_NUMBER)
    pageNum = request.GET.get('page',1)
    print(pageNum)
    newsList = paginator.get_page(pageNum)
    data = []
    for news in newsList:
        str = news2json(news)
        data.append(str)
    return JsonResponse({"toal_num":paginator.num_pages,"data":data},safe=False)

def news2json(news):
    return {
        'newsNum': news.pk,
        'title': news.title,
        'time': news.time,
        'newsImg': news.img,
        'content': news.content,
    }

def getnews():
    # 获取新闻的爬虫
    onepageurl = 'http://sports.sina.com.cn/others/pingpang.shtml'
    data = urllib.request.urlopen(onepageurl).read().decode("utf-8", "ignore")
    pt = '<a target="_blank" href="(https://sports.sina.com.cn/others/pingpang/(.{10})/.*?)">(.*?)<'
    allLink = re.compile(pt).findall(data)
    allLink.reverse()
    addnum = 0
    for i in range(0, len(allLink)):
        # 对爬取的内容进行解析
        thisLink = allLink[i]
        if(not SportsNews.objects.filter(title=thisLink[2])):
            state = 1
            try:
                news = SportsNews()
                news.title = thisLink[2]
                news.time = thisLink[1]
                news.url = thisLink[0]
                detailUrl = news.url
                detail = urllib.request.urlopen(detailUrl).read().decode("utf-8", "ignore")
                imgPt = '<img.*?src="(.*?\.jpg)"'
                contentPt = '</div>(<p>[\d\D]*</p>)[\d\D]*?<div id="left_hzh_ad">|</script>[\d\D]*?(<p>[\d\D]*</p>)[\d\D]*?<div id="left_hzh_ad">'
                imgDetail = re.compile(imgPt).findall(detail)
                if(imgDetail[0]):
                    news.img = 'https:' + imgDetail[0]
                else:
                    state=0
                contentData = re.compile(contentPt).findall(detail)
                pt3 = '<p>\\u3000\\u3000(.*?)</p>'
                if (len(contentData[0]) == 1):
                    for i in contentData:
                        data2 = re.compile(pt3).findall(i)
                        strs = ''
                        for j in data2:
                            strs = strs + '<p>' + str(j) + '</p>'
                elif(len(contentData[0])>1):
                    for i in contentData[0]:
                        data2 = re.compile(pt3).findall(i)
                        strs = ''
                        for j in data2:
                            strs = strs + '<p>' + str(j) + '</p>'
                else:
                    state=0
                if(not strs == ''):
                    news.content = strs
                else:
                    state=0
                if(state!=0):
                    news.save()
                    addnum += 1
            except Exception as e:
                print(e)
    print(addnum)

def detailNews(request,news_pk):
    # pk = request.GET.get('pk','')
    detailNew = get_object_or_404(SportsNews,pk = news_pk)
    context = {}
    context['news'] = detailNew
    return render(request,'sportsnews/detailnews.html',context)

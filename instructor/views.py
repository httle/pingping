from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
# Create your views here.
from .models import Instructor,AppVideo


def instructor_list(request):
    instructor_all = Instructor.objects.all().order_by('-created_time')
    context = {}
    context['instructor_list'] = instructor_all
    return render(request,'instructor/instructor_list.html',context)

def instructor_detail(request,instructor_pk):
    instructor = get_object_or_404(Instructor,pk = instructor_pk)
    context  = {}
    context['instructor'] = instructor
    return render(request,'instructor/instructor_detail.html',context)

def video2json(video):
	return {
		"videourl":video.video_url,
		"posterurl":video.posterImg,
		"title":video.title,
	}

def appVideo_list(request):
	videos = AppVideo.objects.all()
	data = []
	for i in videos:
		strs = video2json(i)
		data.append(strs)

	return JsonResponse({
			'data':data,

		})

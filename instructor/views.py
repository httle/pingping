from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Instructor


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

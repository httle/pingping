from django.contrib import admin

# Register your models here.
from .models import Instructor,AppVideo


@admin.register(Instructor)
class InstructorAdamin(admin.ModelAdmin):
    list_display = ('id','title','created_time')


@admin.register(AppVideo)
class AppVideoAdamin(admin.ModelAdmin):
    list_display = ('id','title')
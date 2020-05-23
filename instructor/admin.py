from django.contrib import admin

# Register your models here.
from .models import Instructor


@admin.register(Instructor)
class InstructorAdamin(admin.ModelAdmin):
    list_display = ('id','title','created_time')
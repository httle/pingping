from django.contrib import admin
from .models import Practice,PracticeImg,MachineControl,CoachSystem
# Register your models here.


@admin.register(Practice)
class PracticeAdamin(admin.ModelAdmin):
	list_display = ('id','user','created_time','practice_num','hit_percent')

@admin.register(PracticeImg)
class PracticeAdamin(admin.ModelAdmin):
	list_display = ('id','practice')

@admin.register(MachineControl)
class MachineControlAdamin(admin.ModelAdmin):
	list_display = ('id','user','machine_num','ifusing')
		
@admin.register(CoachSystem)
class MachineControlAdamin(admin.ModelAdmin):
	list_display = ('id','user','coach')

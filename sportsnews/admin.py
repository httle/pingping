from django.contrib import admin
from .models import SportsNews
# Register your models here.

@admin.register(SportsNews)
class SportsNewsAdamin(admin.ModelAdmin):
    list_display = ('id','title','time','url')
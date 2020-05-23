from django.contrib import admin

# Register your models here.
from .models import BlogType, Blog, BlogImage

# 注册后台的管理

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display=('id','title','blog_type','author','get_read_num','created_time','last_updated_time')

@admin.register(BlogImage)
class BlogImageAdmin(admin.ModelAdmin):
    list_display = ('id','blog')
'''@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
	list_display=('read_num','blog')
'''
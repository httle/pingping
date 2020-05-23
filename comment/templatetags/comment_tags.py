from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm
# 自定义模板标签，要添加__init__.py让其作为一个包
register = template.Library()
#让模板页面可以直接使用模板标签的方法 

@register.simple_tag#注册这个模板标签的方法
def get_comment_count(obj):#得到评论数
	content_type = ContentType.objects.get_for_model(obj)
	return Comment.objects.filter(content_type=content_type,object_id=obj.pk).count()


@register.simple_tag
def get_comment_form(obj):#得到评论的表格
	content_type = ContentType.objects.get_for_model(obj)
	form = CommentForm(initial={'content_type': content_type.model, 'object_id': obj.pk, 'reply_comment_id': 0})
	return form

@register.simple_tag
def get_comment_list(obj):#得到评论列表
	content_type = ContentType.objects.get_for_model(obj)
	comments = Comment.objects.filter(content_type=content_type,object_id=obj.pk, parent=None)
	return comments.order_by('comment_time')
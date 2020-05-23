from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from blog.views import blog2json
from django.utils.html import strip_tags
from notifications.signals import notify
from django.conf import settings

from blog.models import Blog
from .models import Comment
from .forms import CommentForm
# Create your views here.

def update_comment(request):
	# 网站内上传评论
	referer = request.META.get('HTTP_REFERER', reverse('home'))
	comment_form = CommentForm(request.POST, user=request.user)
	data = {}
	# 验证评论格式
	if comment_form.is_valid():
		comment = Comment()
		comment.user = comment_form.cleaned_data['user']
		comment.text = comment_form.cleaned_data['text']
		comment.content_object = comment_form.cleaned_data['comment_object']

		parent = comment_form.cleaned_data['parent']
		if not parent is None:
			comment.root = parent.root if not parent.root is None else parent
			comment.parent = parent
			comment.reply_to = parent.user
		comment.save()

		# 返回数据
		
		data['status'] = 'SUCCESS'
		data['username'] = comment.user.get_nickname_or_username()
		data['comment_time'] = comment.comment_time.timestamp()
		data['text'] = comment.text
		data['content_type'] = ContentType.objects.get_for_model(comment).model
		if not parent is None:
			data['reply_to'] = comment.reply_to.get_nickname_or_username()
		else:
			data['reply_to'] = ''
		data['pk'] = comment.pk
		data['root_pk'] = comment.root.pk if not comment.root is None else ''
	else:
		# return render(request, 'error.html',{'message':comment_form.errors,'redirect_to':referer})
		data['status'] = 'ERROR'
		data['message'] = list(comment_form.errors.values())[0][0]
	return JsonResponse(data)

def appGetComment(request):
	# app获取评论
	blog_pk = request.GET.get('pk',1)
	# print(blog_pk)
	blog = get_object_or_404(Blog,pk=blog_pk)
	blogContentType = ContentType.objects.get_for_model(blog)
	blog_data = blog2json(blog)
	comments = Comment.objects.filter(content_type = blogContentType,object_id = blog_pk,root = None)
	data = []
	position = 0
	for comment in comments.reverse():
		str = comment2json(comment,position)
		data.append(str)
		position+=1
	# print(data)
	return JsonResponse({"blog_data":blog_data,"data": data}, safe=False)

def comment2json(comment,position):
	# 数据转化为json格式
	replyCount = Comment.objects.filter(root = comment).count()
	return {
		'user':comment.getuser(),
		'time':comment.comment_time,
		'text':comment.text,
		'pk':comment.pk,
		'position':position,
		'replyCount':replyCount
	}

def appAddComment(request):
	# app内上传评论
	comment = Comment()
	statue = 1
	user = request.POST.get('user','')
	pk = request.POST.get('pk','')
	text = request.POST.get('comment','')
	type = request.POST.get('type','comment')
	print(text)
	# user = get_object_or_404(User,username = user)
	user = User.objects.get(username = user)
	comment_object = Blog.objects.get(pk = pk)
	if(text.strip() and user and pk):
		comment.user = user
		comment.text = text
		comment.content_object = comment_object
		comment.parent = None
		if(type == "reply"):
			# 如果是回复则要设置其对象和根源
			reply_to_name = request.POST.get('reply_to',"")
			root_pk = request.POST.get('root', "")
			parent_pk = request.POST.get('parent', "")
			reply_to = User.objects.get(username = reply_to_name)
			root = Comment.objects.get(pk = root_pk)
			parent = Comment.objects.get(pk = parent_pk)
			comment.reply_to = reply_to
			comment.root = root
			comment.parent = parent
		comment.save()
		print("内容不为空")
	else:
		statue = 0
		print("内容为空")

	return JsonResponse({"data":{
        'statue':statue,
        'text':"success"
    }},safe=False)


def appReply(request):
	# app内获取回复的方法
	comment_pk = request.GET.get('comment_pk',0)
	print(comment_pk)
	comment = Comment.objects.get(pk = comment_pk)
	comment_data = comment2json(comment,0)
	replys = Comment.objects.filter(root = comment)
	data = []
	for reply in replys.reverse():
		str = reply2json(reply)
		data.append(str)

	return JsonResponse({"comment_data":comment_data,
						 "data":data},safe=False)



def reply2json(reply):
	# 数据转化为json
	return{
		'reply_pk':reply.pk,
		'content':reply.text,
		'user':reply.getuser(),
		'time':reply.comment_time,
		'reply_root':reply.root.pk,
		'reply_parent':reply.parent.pk,
		'reply_to':reply.reply_to.username,
	}



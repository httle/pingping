from django.urls import path
from . import views

urlpatterns = [
	path('update_comment', views.update_comment, name='update_comment'),
	path('app_comment',views.appGetComment),
	path('app_add_comment',views.appAddComment),
	path('app_reply',views.appReply),
]
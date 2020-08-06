from django.urls import path
from . import views

urlpatterns = [
	path('',views.my_notifications,name='my_notifications'),
    path('<int:my_notification_pk>/',views.my_notification,name='my_notification'),
    path('my_notification_delete/',views.my_notification_delete,name='my_notification_delete'),
    path('app_notifications',views.app_notification),
    path('app_notifications_new',views.app_notification_new),
    path('app_notifications_change',views.app_notification_change),
    path('mes_and_chatMes',views.mes_and_chatMes,name='mes_and_chatMes'),
]
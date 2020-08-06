from django.urls import path
from . import views

urlpatterns=[
    path('',views.privateLetter,name='privateLetter'),
    path('chatMessage/',views.chatMessage,name='chatMessage'),
    path('sendChatMes/',views.sendChatMes,name='sendChatMes'),
    path('appChatList',views.appChatList),
    path('appDetailChat',views.appDetailChat),
    path('appChatSend',views.appChatSend),
]
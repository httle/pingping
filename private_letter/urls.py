from django.urls import path
from . import views,view2

urlpatterns=[
    path('',views.privateLetter,name='privateLetter'),
    path('chatMessage/',views.chatMessage,name='chatMessage'),
    path('sendChatMes/',views.sendChatMes,name='sendChatMes'),
    path('webNotify/',views.webChatNotify,name='webNotify'),
    path('appChatList',views.appChatList),
    path('appDetailChat',views.appDetailChat),
    path('appChatSend',views.appChatSend),
    path('startChat',view2.startChat,name='startChat'),
    path('appStartChat',view2.appStartChat),
]
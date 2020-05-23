from django.urls import path
from . import views

urlpatterns=[
    path('',views.sportsNewsList,name='sportsNewsList'),
    path('<int:news_pk>',views.detailNews,name='detailNews'),
    path('appsportsnews',views.appSportsNews),

]
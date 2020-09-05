from django.urls import path
from . import views,views2,views3

urlpatterns=[
    path('appcontrol',views.appControl),
    path('test',views.test),
    path('uploadData',views.uploadPracData),
    path('practice_list',views2.practice_list,name='practice_list'),
    path('<int:practice_pk>',views2.practice_detail,name='practice_detail'),
    path('app_practice',views2.app_practice),
    path('machineUsing',views3.machineUsing),
    path('learnerList',views3.learnerList),
    path('coachSet',views3.coachSet),
]
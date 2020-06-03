from django.urls import path
from . import views

urlpatterns=[
    path('appcontrol',views.appControl),
    path('test',views.test),
    path('uploadData',views.uploadPracData),
]
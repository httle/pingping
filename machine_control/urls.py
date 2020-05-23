from django.urls import path
from . import views

urlpatterns=[
    path('appcontrol',views.appControl),
]
"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from . import views
urlpatterns = [
    path('',views.home2,name='home'),
    path('count',views.home,name='count'),
    path('admin/', admin.site.urls),
    path('ckeditor/',include('ckeditor_uploader.urls')),
    path('blog/',include('blog.urls')),
    path('comment/',include('comment.urls')),
    path('likes',include('likes.urls')),
    path('user/',include('user.urls')),
    path('notifications/',include('notifications.urls',namespace='notifications')),
    path('mynotifications/',include('my_notifications.urls'),name='notifications'),
    path('my_notifications/',include('my_notifications.urls')),
    path('search/', views.search,name='search'),
    path('instructor_list/',include('instructor.urls')),
    path('sportsnews/',include('sportsnews.urls')),
    path('appcontrol/',include('machine_control.urls')),
    path('privaletter/',include('private_letter.urls')),
    path(r'media/(?P<path>.*)',serve,{'document_root':settings.MEDIA_ROOT}),

]

urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.BLOGIMG_URL, document_root = settings.BLOGIMG_ROOT)
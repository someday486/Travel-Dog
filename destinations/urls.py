from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from . import views
app_name = 'DT'
urlpatterns = [
    re_path(r"(\d+)/$", views.location, name='loca'),
    re_path(r"(\d+)/([0-9a-zA-Zㄱ-힣 %()_.-]+)/([0-9a-zA-Zㄱ-힣 %()_.-]+)/$", views.addtrip),
    re_path(r"addmyplace/(\d+)/([0-9a-zA-Zㄱ-힣 %()_.-]+)/([0-9a-zA-Zㄱ-힣 %()_.-]+)/$",views.addmyplace),
    
]
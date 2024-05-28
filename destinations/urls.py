from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.location),
    re_path(r"([0-9a-zA-Zㄱ-힣 %()_.-]+)/([0-9a-zA-Zㄱ-힣 %()_.-]+)/$", views.addtrip),
    
]
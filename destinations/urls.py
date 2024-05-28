from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index),
    
]
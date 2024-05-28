from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('index/',views.index),
    path('detail/<int:userId>/',views.detail),
    path('tripDetail/<int:userId>/<borderId>/',views.tripDetail),
]
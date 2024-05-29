from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('index/',views.index),
    path('detail/<int:tripId>/',views.detail),
    path('tripDetail/<int:tripId>/',views.tripDetail),
]
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/',views.index),
    path('detail/<int:userId>/',views.detail),
    path('tripDetail/<int:tripId>/',views.tripDetail),
    path('upload/', views.upload_file, name='upload_file'),
    path('add/<int:borderId>/',views.add),
] 
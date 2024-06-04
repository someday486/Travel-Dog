from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'EP'

urlpatterns = [
    path("", views.index),
    path('index2/<int:trip_id>/', views.index2, name="E"),
    path('fileremove/<trip_detail_id>', views.file_remove)
]

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from . import views


urlpatterns = [
<<<<<<< HEAD
    path("", views.myplace),
    path("addmyplace",views.addmyplace),
=======
    path("", views.myplace),    
    
>>>>>>> fb7c23d54dba6485d2bc0fcc1fa9d1627698467d
]
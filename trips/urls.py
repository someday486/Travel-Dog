from django.urls import path, re_path
from . import views

app_name = 'trips'

urlpatterns= [
    path('index/', views.index, name="I"),
    path('next_page/', views.next_page, name='next_page'),
]
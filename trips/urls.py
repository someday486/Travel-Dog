from django.urls import path, re_path
from . import views

app_name = 'trips'

urlpatterns= [
    path('index/', views.index, name="I"),
    re_path(r'next_page/(\d+)', views.next_page, name='next_page'),
]
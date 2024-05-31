from django.urls import path, re_path
from . import views

app_name = 'managetrip'

urlpatterns= [
    path('', views.index, name="I"),
    path('<int:trip_id>/', views.manage, name="M"),
]
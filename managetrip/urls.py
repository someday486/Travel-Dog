from django.urls import path, re_path
from . import views

app_name = 'managetrip'

urlpatterns= [
    path('', views.index, name="I"),
    path('<int:trip_id>/', views.manage, name="M"),
    path('deletetrip/<int:trip_id>/', views.deletetrip, name="D"),
    path('deletetripdetail/<int:trip_id>/<int:tripdetail_id>/', views.deletetripdetail, name="DD"),
]
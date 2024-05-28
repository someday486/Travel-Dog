from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from . import settings

urlpatterns = [
    path('<str:trip_id>/', views.expense_list, name='expense_list'),
    path('<str:trip_id>/add/', views.add_expense, name='add_expense'),
    path('<str:trip_id>/edit/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('<str:trip_id>/delete/<int:expense_id>/', views.delete_expense, name='delete_expense'),
    path('<str:trip_id>/send/', views.send_to_trips_detail, name='send_to_trips_detail'),
]

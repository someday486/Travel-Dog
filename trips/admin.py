from django.contrib import admin
from .models import Region, Destination, Trip, TripDetail

class TripAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'region', 'start_date', 'end_date']

class TripDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'trip', 'day', 'destination', 'expense']

admin.site.register(Region)
admin.site.register(Destination)
admin.site.register(Trip, TripAdmin)
admin.site.register(TripDetail, TripDetailAdmin)
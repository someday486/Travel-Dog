from django.contrib import admin
from .models import Region, Destination, Trip, TripDetail

admin.site.register(Region)
admin.site.register(Destination)
admin.site.register(Trip)
admin.site.register(TripDetail)
from django.db import models
from django.contrib.auth.models import User

class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Destination(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} - {self.region.name} ({self.start_date} to {self.end_date})'

class TripDetail(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    day = models.IntegerField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    expense = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.trip} - Day {self.day}: {self.destination.name}'

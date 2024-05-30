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
    def duration(self):
        return (self.end_date - self.start_date).days


class TripDetail(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    day = models.IntegerField()
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    expense = models.DecimalField(max_digits=10, decimal_places=2,null=False)
    context = models.TextField(null=True)
    hashtag = models.TextField()   #해시태그 저장/ 초기화시 아무 데이터도 안 넣을 수 있다.

    def __str__(self):
        return f'{self.trip} - Day {self.day}: {self.destination.name}, {self.expense}'

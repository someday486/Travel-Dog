from django.db import models
from django.contrib.auth.models import User
from trips.models import Destination

class Myplace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)

    def __str__(self):
       return f'{self.destination}'
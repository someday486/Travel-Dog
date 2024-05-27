from django.db import models

# Create your models here.

class Review(models.Model):
    userId= models.CharField(max_length=100)
    tripId= models.CharField(max_length=100)
    viewsCnt= models.IntegerField(null=False)
    contentId= models.CharField(max_length=100)
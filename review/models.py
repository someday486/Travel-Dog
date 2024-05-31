from django.db import models
from trips.models import Trip, TripDetail
from PIL import Image

# Create your models here.

class Border(models.Model):
    trip_detail = models.ForeignKey(TripDetail, on_delete=models.CASCADE)
    제목 = models.CharField(max_length=255, blank=False, null=False)
    작성일 = models.DateTimeField(null=False)
    조회수 = models.IntegerField(null=False, default=0)

    def __str__(self):
        return f'({self.trip_detail})'

class BorderImage(models.Model):
    border = models.ForeignKey(Border,related_name='images',on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'Image for {self.border}'
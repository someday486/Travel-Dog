from django.db import models
from trips.models import Trip, TripDetail
from PIL import Image

# Create your models here.

class Border(models.Model):
    trip_detail = models.ForeignKey(TripDetail, on_delete=models.CASCADE)
    제목 = models.CharField(max_length=255, blank=False, null=False)
    작성일 = models.DateTimeField(null=False)
    조회수 = models.IntegerField(null=False, default=0)
    이미지 = models.ImageField(upload_to='images/', null=True, blank=True)
    hashtag = models.TextField()   #해시태그 저장/ 초기화시 아무 데이터도 안 넣을 수 있다.

    def __str__(self):
        return f'({self.trip_detail})'

from django.db import models
from trips.models import Trip

# Create your models here.

class Border(models.Model):
    trip=models.ForeignKey(Trip, on_delete=models.CASCADE,default=0)
    제목 = models.CharField(max_length=255, blank=False, null=False) 
    작성자 = models.CharField(max_length=255, blank=False, null=False)
    내용 = models.TextField(null=False)
    작성일 = models.DateTimeField(null=False)
    조회수 = models.IntegerField(null=False, default=0)
    # default : 객체 생성할 때 기본값
    # 댓글수 = models.IntegerField(null=False, default=0)
    좋아요 = models.IntegerField(null=False, default=0)
    
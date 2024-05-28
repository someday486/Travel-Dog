from django.db import models


# Create your models here.

class Review(models.Model):
    userId= models.IntegerField(null=False)
    tripId= models.CharField(max_length=100)
    viewsCnt= models.IntegerField(null=False)
    contentId= models.CharField(max_length=100) 

class Border(models.Model):
    제목 = models.CharField(max_length=255, blank=False, null=False) 
    작성자 = models.CharField(max_length=255, blank=False, null=False)
    내용 = models.TextField(null=False)
    작성일 = models.DateTimeField(null=False)
    조회수 = models.IntegerField(null=False, default=0)
    # default : 객체 생성할 때 기본값
    댓글수 = models.IntegerField(null=False, default=0)
    좋아요 = models.IntegerField(null=False, default=0)
    
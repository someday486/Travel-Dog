from django.shortcuts import render,get_object_or_404,redirect
from review.models import Border
from trips.models import TripDetail, Trip, Region, Destination
from datetime import datetime


# Create your views here.


def index(request):
    userId=request.user.id
    query=request.GET.get('topic','')
    if query:
        border=Border.objects.filter(내용__icontains=f'#{query}')
    else:
        trips=Trip.objects.all()  # 해시태그로 검색한거 아니면 일정 다 가져오기

    content={
        'trips':trips,
        'userId':userId,
        'topic':query,
    }
    return render(request,'review/index.html',content);

def detail(request,tripId): # 해당 사용자의 전체 게시물 확인
    userId=request.user.username
    trips=Trip.objects.filter(user=tripId)
    content={
        'trips':trips,
        'userId':userId,
    }
    return render(request,'review/detail.html',content)

def tripDetail(request,tripId):
    trip=get_object_or_404(Trip,id=tripId) #borderId가 동일한 게시글 불러오기 
    tripdetails=TripDetail.objects.filter(trip=trip)
    content = {
        'trip':trip,
        'tripdetails':tripdetails,
    }
    return render(request, 'review/tripDetail.html', content)

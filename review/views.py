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
        border=Border.objects.all()

    content={
        'border':border,
        'userId':userId,
        'topic':query,
    }
    return render(request,'review/index.html',content);

def detail(request,userId): # 사용자의 전체 게시물 확인
    user=request.user.id  #현재 로그인한 사용자
    # 그중에서 해당 userId를 가진 게시물만 filter 하기
    borders = Border.objects.filter(trip__user=user)  # 로그인한 사용자와 trip의 user와 같은 게시물만 필터링 (게시물들)
    border=borders.first()
    userId=border.trip.user
    content={
        'borders':borders,
        'userId':userId,
        'user':user,
    }

    return render(request,'review/detail.html',content)

def tripDetail(request,userId,borderId):
    now=datetime.now()
    border=get_object_or_404(Border,id=borderId) #borderId가 동일한 게시글 불러오기 
    content = {
        'border': border,
    }
    return render(request, 'review/tripDetail.html', content)

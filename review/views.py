import os
from django.shortcuts import render,get_object_or_404,redirect
from review.models import Border
from trips.models import TripDetail, Trip, Region, Destination
from datetime import datetime
from PIL import Image
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.


def index(request):
    userId=request.user.id
    query=request.GET.get('topic','')
    if query:
        borders=Border.objects.filter(내용__icontains=f'#{query}')
        content={
            'borders':borders,
            'userId':userId,
            'topic':query,
        }
    else:
        trips=Trip.objects.all()  # 해시태그로 검색한거 아니면 일정 다 가져오기
        content={
            'trips':trips,
            'userId':userId,
        }
    return render(request,'review/index.html',content);

def detail(request,userId): # 해당 사용자의 전체 게시물 확인
    userName=request.user.username
    trips=Trip.objects.filter(user=userId)
    content={
        'trips':trips,
        'userName':userName,
    }
    return render(request,'review/detail.html',content)

def tripDetail(request,tripId):
    trip=get_object_or_404(Trip,id=tripId) #tripId 가 동일한 글 불러오기
    # borders=Border.objects.all()  # 게시판 전체 객체 가져오기 (없어도 에러발생하지 않음)
    tripdetails=TripDetail.objects.filter(trip=trip) # 현재 trip과 같은 객체를 가진 tripdetail들을 가져옴
    borders = Border.objects.filter(trip_detail__in=tripdetails) # 해당 trip의 border 객체만 필터링

    if not borders.exists():
        return render(request,'review/add.html',{
            'message': '여행일지가 없는 Trip입니다. add페이지로 이동할게요',
            'tripdetails':tripdetails,
        }); 

    borderList=findBorder(tripdetails, borders);
    fileList= fileFind(trip);

    content = {
        'trip': trip,
        'tripdetails': tripdetails,
        'fileList': fileList,
        'borderList': borderList,
    }
    return render(request,'review/tripDetail.html',content);


def add(request, borderId):
    border=Border.objects.get(id=borderId)
    content={
        'border':border,
    }
    return render(request,'review/add.html',content);


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        try:
            trip_id = request.POST['trip_id']
            day = request.POST['day']
            file = request.FILES['file']  # 사용자가 업로드한 파일

            trip = Trip.objects.get(id=trip_id)
            trip_folder = os.path.join(settings.MEDIA_ROOT, str(trip_id))
            day_folder = os.path.join(trip_folder, f'day_{day}')
            os.makedirs(day_folder, exist_ok=True)  # 경로가 존재하지 않으면 새로운 폴더 생성

            file_path = os.path.join(day_folder, file.name)  # 파일 저장 경로 생성
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():  # 파일을 작은 조각으로 나누어 씀
                    destination.write(chunk)

            return JsonResponse({'status': 'success', 'file_path': file_path})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

# def add(request,tripDetailId):
#     return render(request,'review/border.html',content);

def fileFind(trip):
    file_path = os.path.join(settings.MEDIA_ROOT, str(trip.id));
    fileNames =  os.listdir(file_path)
    print(fileNames)
    tripdetails=TripDetail.objects.filter(trip=trip)
    daydetail = {} 
    for t in tripdetails:
        daydetail[t.day] = t.id
 
    fileList={}
    for f in fileNames:
        file_path1=os.path.join(file_path,f)
        if daydetail.get(int(f)):
            fileList[f] = {daydetail.get(int(f)) : os.listdir(file_path1)}

    return fileList;

def findBorder(tripdetails, borders): # 디테일id에 맞는 border id찾기
    border=[]
    for t in tripdetails:
        for b in borders:
            if t == b.trip_detail:
                border.append(t)
    return border;   # 디테일에서 입력한 border 리스트 전달

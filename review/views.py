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

def detail(request,tripId): # 해당 사용자의 전체 게시물 확인
    userId=request.user.username
    trips=Trip.objects.filter(user=tripId)
    content={
        'trips':trips,
        'userId':userId,
    }
    return render(request,'review/detail.html',content)

def tripDetail(request,tripId):
    trip=get_object_or_404(Trip,id=tripId) #tripId 가 동일한 글 불러오기
    tripdetails=TripDetail.objects.filter(trip=trip)
    fileList= fileFind(trip)
    print(fileList)
    content = {
        'trip':trip,
        'tripdetails':tripdetails,
        'fileList':fileList,
     }
    return render(request, 'review/tripDetail.html', content)


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

# def add(request,tripdetailId):
    # tripdetailId  
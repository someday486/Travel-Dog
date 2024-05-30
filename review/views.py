import os, re
from django.shortcuts import render, get_object_or_404, redirect
from review.models import Border
from trips.models import TripDetail, Trip
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# Create your views here.

def extract_hashtags(text):
    if text:
    # tripdetail 객체에서 해시태그 내용만 골라낸다
        return re.findall(r'#\w+', text);

def index(request):
    userId=request.user.id
    query=request.GET.get('topic','')
    if query:
        tripdetails=TripDetail.objects.filter(context__icontains=f'#{query}')
        content={
            'tripdetails':tripdetails,
            'userId':userId,
            'topic':query,
        }
    else:
        trips=Trip.objects.all()  # 해시태그로 검색한거 아니면 일정 다 가져오기
        detailList=findTripDetails(trips);
        content={
            'trips':trips,
            'userId':userId,
            'detailList':detailList,
        }
    return render(request,'review/index.html',content);

def detail(request,userId): # tripdetailId를 넘겨줘야 한다.
    userName=request.user.username
    trips=Trip.objects.filter(user=userId)
    # 해당 trips에 맞는 tripdetail id를 찾기
    detailList=findTripDetails(trips);
    for trip,details in detailList.items():
        borderList={}
        for detail in details:
            border=Border.objects.get(trip_detail=detail) # detail 객체와 동일한 border를 끌어온다
    content={
        'trips':trips,
        'userName':userName,
        'detailList':detailList,
    }
    return render(request,'review/detail.html',content)

def findTripDetails(trips):
    detailList={}
    for t in trips:
        tripdetails=TripDetail.objects.filter(trip=t)
        detailList[f'{t}']=tripdetails   # trip에 대한 detail 객체들 저장
    return detailList;  # {trip1:tripdetail1 tripdetail2, trip2:....}

def findBorder(tripdetails, borders): # 디테일id에 맞는 border id찾기
    borderList=[]
    for t in tripdetails:
        for b in borders:
            if t == b.trip_detail:
                borderList.append(b)
    return borderList;   # 디테일에서 입력한 border 리스트 전달

def tripDetail(request,tripId):
    userId=request.user.id
    trip=get_object_or_404(Trip,id=tripId) #tripId 가 동일한 글 불러오기
    tripdetails=TripDetail.objects.filter(trip=trip) # 현재 trip과 같은 객체를 가진 tripdetail들을 가져옴

    borders = Border.objects.filter(trip_detail__in=tripdetails) 

    borderList=findBorder(tripdetails, borders);
    print(borderList)
    try:
        fileList= fileFind(trip);
        content = {
            'trip': trip,
            'tripdetails': tripdetails,
            'fileList': fileList,
            'borderList': borderList,
        }
        return render(request,'review/tripDetail.html',content);
    except Exception as e:
        print(e)
        content = {
            'trip': trip,
            'tripdetails': tripdetails,
            'borderList': borderList,
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


def add(request, tripdetailId):
    tripdetail = get_object_or_404(TripDetail, id=tripdetailId)
    now = datetime.now()
    tripId=tripdetail.trip.id
    
    if request.method == "POST":
        # POST 요청으로부터 데이터를 가져옵니다.
        title = request.POST.get('title')
        # hashtag = request.POST.get('hashtag')
        form_context = request.POST.get('form_context')
        image = request.FILES.get('image')  # 파일은 FILES에서 가져옵니다.

        #수정된 tripdetail 객체 업데이트
        tripdetail.context=form_context
        tripdetail.save()

        # Border 객체를 생성하여 저장합니다.
        border = Border(
            trip_detail=tripdetail,
            제목=title,
            작성일=now,
            이미지=image,
            # hashtag=hashtag
        )
        border.save()


        # 저장 후 리디렉션합니다.
        return redirect(f'/review/tripDetail/{tripId}/')  # 다시 tripdetail 페이지로 이동

    content = {
        'tripdetail': tripdetail,
        'now': now,
    }
    return render(request, 'review/add.html', content)


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



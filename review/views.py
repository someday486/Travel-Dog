import os, re
from django.shortcuts import render, get_object_or_404, redirect
from review.models import Border, BorderImage
from trips.models import TripDetail, Trip
from datetime import datetime
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import urllib.parse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def delete_image(request, borderId, imageId):
    # 이미지 URL을 디코딩합니다.
    # decoded_url = urllib.parse.unquote(imageId)
    # image_path = os.path.join(settings.MEDIA_ROOT, decoded_url.replace(settings.MEDIA_URL, '').lstrip('/'))
    print(f'image_url: {imageId}')
    # print(f'decode_url: {decoded_url}')
    # print(f'image_path: {image_path}')
    
    try:
        # Border 및 관련된 TripDetail 객체를 가져옵니다.
        border = get_object_or_404(Border, id=borderId)
        tripDetail = get_object_or_404(TripDetail, id=border.trip_detail.id)
        
        #ExpenseDetail.objects.filter(trip_detail__in=trip_details).delete()  

        # 데이터베이스에서 BorderImage 객체 삭제
        borderImg = get_object_or_404(BorderImage, id=imageId)
        print(f'borderImg: {borderImg}')
        borderImg.delete()

        # 이미지 파일 삭제
        # if default_storage.exists(image_path):
        #     default_storage.delete(image_path)
        
        # 성공적으로 삭제된 경우 add 페이지로 리디렉션
        return redirect(f'/review/add/{tripDetail.id}/')
    
    except Exception as e:
        # 에러 발생 시 메시지를 생성합니다.
        return JsonResponse({'success': False, 'error': str(e)})


@login_required    
def extract_hashtags(text):
    if text:
    # tripdetail 객체에서 해시태그 내용만 골라낸다
        return re.findall(r'#\w+', text);

def index(request):
    userId = request.user.id
    query = request.GET.get('topic', '')
    print('쿼리:', query)
    
    trips = Trip.objects.all()
    imageList = {}  # {trip1: [imgurl1, imgurl2, ...], trip2: [imgurl1, imgurl2, ...], ...}
    
    # 각 trip에 맞는 이미지 리스트 생성
    for trip in trips:
        tripDetails = TripDetail.objects.filter(trip_id=trip.id)
        for detail in tripDetails:
            try:
                imgs = []
                border = Border.objects.get(trip_detail=detail)
                images = BorderImage.objects.filter(border_id=border.id)
                for img in images:
                    imgs.append(img.image.url)
                imageList[trip.id] = imgs
            except:
                imageList[trip.id] = []
    
    if query:
        tripdetails = TripDetail.objects.filter(context__icontains=f'#{query}')
        detailList = {}  # {tripId: [details]}
        
        for d in tripdetails:
            if d.trip.id not in detailList:
                detailList[d.trip.id] = []
            detailList[d.trip.id].append(d)
        
        content = {
            'detailList': detailList,
            'userId': userId,
            'topic': query,
            'imageList': imageList,
        }
        return render(request, 'review/index.html', content)
        
    else:
        trips_len =  range(4-len(trips) % 4)
        content = {
            'trips': trips,
            'userId': userId,
            'imageList': imageList,
            'trips_len':trips_len,
        }
        return render(request, 'review/index.html', content)

@login_required
def detail(request, userId):  # tripdetailId를 넘겨줘야 한다.
    userName=request.user.username
    trips = Trip.objects.filter(user_id=userId)
    imageList={}  # {trip1 : imgurl1, trip2: imgurl2, ...}
    for trip in trips:
        tripDetails = TripDetail.objects.filter(trip_id=trip.id)
        for detail in tripDetails:
            try:
                imgs=[]
                border=Border.objects.get(trip_detail=detail)
                images=BorderImage.objects.filter(border_id=border.id)
                for img in images:
                    imgs.append(img.image.url)
                imageList[trip.id]=imgs
            except:
                imageList[trip.id]=[]
  
    
    content = {
        'trips': trips,
        'userId': userId,
        'userName':userName,
        'imageList':imageList,
    }
    return render(request, 'review/detail.html', content)

@login_required
def findTripDetails(trips):
    detailList={}
    for t in trips:
        tripdetails=TripDetail.objects.filter(trip=t)
        detailList[t]=tripdetails   # trip에 대한 detail 객체들 저장
    return detailList;  # {trip1:tripdetail1 tripdetail2, trip2:....}

@login_required
# 각 디테일과 일치하는 border 객체 반환
def findBorder(tripdetails, borders):
    borderList = []
    for tripdetail in tripdetails:
        try:
            border = borders.get(trip_detail=tripdetail)
            borderList.append(border)
        except Border.DoesNotExist:
            continue
    return borderList;

@login_required
# 각 TripDetail에 해당하는 BorderImage URL 정보를 딕셔너리 형태로 반환
def findImage(tripdetails, borderList):
    images = {}
    for b in borderList:
        tripdetail = tripdetails.get(id=b.trip_detail.id) 
        imgs = BorderImage.objects.filter(border=b)  # border에 해당되는 borderImage 객체들만 필터링
        image_urls = [i.image.url for i in imgs]  # 이미지 객체의 URL 리스트 생성
        images[tripdetail.id] = image_urls  # tripdetail ID를 키로 사용하여 딕셔너리에 저장


    return images;

@login_required
def add(request, tripdetailId):
    tripdetail = get_object_or_404(TripDetail, id=tripdetailId)
    now = datetime.now()
    tripId = tripdetail.trip.id
    defaultImg_path = os.path.join(settings.MEDIA_URL, 'images', 'dog.jpg')

    is_owner = request.user == tripdetail.trip.user

    if request.method == "POST" and is_owner:
        # 기존 Border 객체를 가져오거나 없으면 새로 생성합니다.
        border, created = Border.objects.get_or_create(
            trip_detail=tripdetail,
            defaults={
                '제목': request.POST.get('title', ''),
                '작성일': now,
                '조회수': 0,
            }
        )
        
        # 만약 기존 Border 객체가 있다면 제목과 작성일을 업데이트합니다.
        if not created:
            border.제목 = request.POST.get('title', '')
            border.작성일 = now
            border.save()

        # tripdetail의 내용을 업데이트합니다.
        tripdetail.context = request.POST.get('form_context', '')
        tripdetail.save()

        # 이미지 파일이 존재하는 경우 BorderImage 객체를 생성합니다.
        images = request.FILES.getlist('images')
        if images:
            folder_path = os.path.join(settings.MEDIA_ROOT, 'images', str(tripdetail.id))
            os.makedirs(folder_path, exist_ok=True)  # 폴더가 존재하지 않으면 생성

            for image in images:
                image_path = os.path.join(folder_path, image.name)
                with open(image_path, 'wb+') as destination:
                    for chunk in image.chunks():
                        destination.write(chunk)
                BorderImage.objects.create(border=border, image=os.path.join('images', str(tripdetail.id), image.name))

        return redirect(f'/review/tripDetail/{tripId}/')

    # GET 요청 처리 또는 사용자가 소유자가 아닌 경우
    try:
        border = Border.objects.get(trip_detail=tripdetail)
    except Border.DoesNotExist:
        border = None

    if border:
        border_images=BorderImage.objects.filter(border=border)
        if border_images:
        # image_urls = [i.image.url for i in border_images]  # 이미지 객체 리스트 반환
            images = [i for i in border_images]  # 이미지 객체 리스트 반
            content = {
            'border': border,
            'borderImages': border_images,  # border 이미지 객체 반환 쿼리셋
            'tripdetail': tripdetail,
            'now': now,
            'tripId': tripId,
            'userCheck': is_owner,
            'images':images,
                }
            return render(request, 'review/add.html', content)
        else:
            content = {
            'border': border,
            'borderImages': border_images,  # border 이미지 객체 반환 쿼리셋
            'tripdetail': tripdetail,
            'now': now,
            'tripId': tripId,
            'userCheck': is_owner,
            }
            return render(request, 'review/add.html', content)
    else:
        content = {
            # 'border': border,
            # 'borderImages': border_images,  # border 이미지 객체 반환 쿼리셋
            'tripdetail': tripdetail,
            'now': now,
            'tripId': tripId,
            'userCheck': is_owner,
        }
        return render(request, 'review/add.html', content)

@login_required
def tripDetail(request,tripId):  # day 순서로 정렬 필요
    userId=request.user.id
    trip=get_object_or_404(Trip,id=tripId) #tripId 가 동일한 글 불러오기
    tripdetails=TripDetail.objects.filter(trip=trip).order_by('day') # 현재 trip과 같은 객체를 가진 tripdetail들을 가져옴
    
    # day: tripdetail 객체 딕셔너리
    detailDict = {detail.day: detail for detail in tripdetails}
    print('정렬된 데이터:', detailDict)
    # detailDict={}
    # for detail in tripdetails:
    #     detailDict[detail]=detail.day
    # print('원본:',detailDict)

    # detailDict_2= sorted(detailDict.items(), key=lambda x: x[1])
    # print('전송할 데이터:',detailDict_2)
    # detailDict_3={}
    # for d,k in detailDict_2:
    #     detailDict_3[k]=d
    # print('detailDict_3:',detailDict_3)

    borders = Border.objects.filter(trip_detail__in=tripdetails) 
    borderList=findBorder(tripdetails, borders);  # 각 디테일과 일치하는 border 객체반환
    try:
        imageUrls= findImage(tripdetails, borderList);
        content = {
            'trip': trip,
            # 'tripdetails': tripdetails,
            'detailDict':detailDict,
            'imageUrls': imageUrls,
            'borderList': borderList,
            # 'defaultImg_path': settings.DEFAULT_IMAGE_URL,  # 기본 이미지 경로 전달
        }
        return render(request,'review/tripDetail.html',content);
    except Exception as e:
        content = {
            'trip': trip,
            'detailDict': detailDict,
            'borderList': borderList,
            # 'defaultImg_path': settings.DEFAULT_IMAGE_URL,  # 기본 이미지 경로 전달
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








    

    
     





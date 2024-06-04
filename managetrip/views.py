from django.shortcuts import render
from trips.models import TripDetail, Trip
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
import shutil
import os

@login_required
def index(request):
    username = request.user.username
    trip_list = list(Trip.objects.filter(user=request.user))
    content = {
        'username':username,
        'trip_list':trip_list,
    }
    return render(request, 'managetrip/index.html', content)

@login_required
def manage(request, trip_id):
    if request.method == 'POST':
        tripdetail = TripDetail()
        content = {
            'trip_info' : trip_info,
            'trip_detail' : trip_detail,
        }
        return render(request, 'managetrip/manage.html', content)
    else:
        if request.user.is_active:  
            trip_info = Trip.objects.get(id=trip_id)
            trip_detail = TripDetail.objects.filter(trip=trip_info).order_by('day')
            content = {
                'trip_info' : trip_info,
                'trip_detail' : trip_detail,
            }
            return render(request, 'managetrip/manage.html', content);

@login_required
def deletetrip(request, trip_id):
    # DB 삭제 : 클래스객체.objects.get(pk=값).delete()
    trip = Trip.objects.get(id=trip_id);
    content = {
        'trip' : trip
    }
    trip.delete()

    # os.remove(파일삭제)
    # os.rmdir(폴더삭제 - 빈폴더만 삭제가능)
    path = os.path.join(settings.MEDIA_ROOT, str(trip_id))
    if os.path.isdir(path):
        # dirList = os.listdir(path)
        # for f in dirList:
        #     os.remove(path + "/" + f)
        # os.rmdir(path)
        shutil.rmtree(path)
    return render(request, 'managetrip/delete.html', content)

@login_required
def deletetripdetail(request, trip_id, tripdetail_id):
    # DB 삭제 : 클래스객체.objects.get(pk=값).delete()
    trip_detail = TripDetail.objects.get(id=tripdetail_id)

    trip_detail.delete()

    # os.remove(파일삭제)
    # os.rmdir(폴더삭제 - 빈폴더만 삭제가능)
    path = os.path.join(settings.MEDIA_ROOT, (str(trip_id) + "/" + str(tripdetail_id)))
    if os.path.isdir(path):
        # dirList = os.listdir(path)
        # for f in dirList:
        #     os.remove(path + "/" + f)
        # os.rmdir(path)
        shutil.rmtree(path)
    content = {
        'trip_detail' : trip_detail,
        'trip_id' : trip_id,
    }
    return render(request, 'managetrip/delete2.html', content)
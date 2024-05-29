from django.shortcuts import render, redirect, get_object_or_404
from trips.models import TripDetail, Trip, Region
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    username = request.user.username
    trip_list = list(Trip.objects.filter(user=request.user))
    content = {
        'username':username,
        'trip_list':trip_list,
    }
    return render(request, 'expense/index.html', content)

def index2(request, trip_id):
    trip_info = Trip.objects.get(id=trip_id)
    trip_detail = TripDetail.objects.filter(trip=trip_info)
    print(trip_info)
    print(trip_detail)
    content = {
        'trip_info' : trip_info,
        'trip_detail' : trip_detail,
    }
    return render(request, 'expense/index2.html', content)
from django.shortcuts import render
from trips.models import TripDetail, Trip
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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
            trip_detail = TripDetail.objects.filter(trip=trip_info)
            content = {
                'trip_info' : trip_info,
                'trip_detail' : trip_detail,
            }
            return render(request, 'managetrip/manage.html', content);
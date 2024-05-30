from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Region, Trip, TripDetail, Destination
import datetime


@login_required
def index(request):
    if request.method == 'POST':
        region_id = request.POST.get('selected_region')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        region = Region.objects.get(id=region_id)
        trip = Trip.objects.create(user=request.user, region=region, start_date=start_date, end_date=end_date)
        trip_id =trip.id
        return redirect('trips:next_page', trip_id)

    regions = Region.objects.all()
    return render(request, 'trips/index.html', {'regions': regions})

@login_required
def next_page(request,trip_id):
    if request.method == 'GET':
        trip = Trip.objects.get(id=trip_id)
        tripdetail = TripDetail.objects.filter(trip=trip)
        destination = Destination.objects.all()

        # 날짜 범위
        start_date = trip.start_date
        end_date = trip.end_date
        delta = end_date - start_date
        index = str(trip).find('-')
        head = str(trip)[index+1:].strip()

        # 날짜 리스트
        # trip_dates = []
        # for i in range(delta.days + 1):
        #     day = start_date + datetime.timedelta(days=i)
        #     trip_dates.append(day)
        # day = len(trip_dates)


        trip_dates = {}
        for i in range(1,delta.days + 2):
            day = start_date + datetime.timedelta(days=i)
            trip_dates[i] = day
        day = len(trip_dates)


        content = {
            'trip': trip,
            'tripdetail': tripdetail,
            'destination': destination,
            'day': day, #스피너 end값
            'trip_dates': trip_dates, #Trip-Detail 표의 날짜
            'trip_id': trip_id,
            'head': head, #상위제목
        }
        return render(request, 'trips/next_page.html',content)  # 다음 페이지로 이동
    
    elif request.method == 'POST':
        tripdetail = TripDetail()
        tripdetail.trip = Trip.objects.get(id=trip_id)
        tripdetail.day = request.POST['day']
        tripdetail.destination = Destination.objects.get(id=request.POST.get('d_id'))
        tripdetail.expense = request.POST['expense']
        tripdetail.context = request.POST['context']
        tripdetail.save()


        return redirect('trips:next_page', trip_id)
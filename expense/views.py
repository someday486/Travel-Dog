from django.shortcuts import render, redirect, get_object_or_404
from trips.models import TripDetail, Trip
from expense.models import ExpenseDetail
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
    if request.method == 'POST':
        expensedetail = ExpenseDetail()
        # expensedetail.trip_detail = request.POST.get()
        expensedetail.memo = request.POST.get("memo")
        # expensedetail.receipt = request.POST.get("receipt")
        trip_info = Trip.objects.get(id=trip_id)
        trip_detail = TripDetail.objects.filter(trip=trip_info)
        total_expense = sum(x.expense for x in trip_detail)
        print(total_expense)
        content = {
            'trip_info' : trip_info,
            'trip_detail' : trip_detail,
            'total_expense':total_expense,
        }
        return render(request, 'expense/index2.html', content)
    else:
        if request.user.is_active:  
            trip_info = Trip.objects.get(id=trip_id)
            trip_detail = TripDetail.objects.filter(trip=trip_info)
            total_expense = sum(x.expense for x in trip_detail)
            print(total_expense)
            content = {
                'trip_info' : trip_info,
                'trip_detail' : trip_detail,
                'total_expense':total_expense,
            }
            return render(request, 'expense/index2.html', content);
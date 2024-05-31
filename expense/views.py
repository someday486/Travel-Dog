from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from trips.models import TripDetail, Trip
from expense.models import ExpenseDetail
from django.contrib.auth.models import User
from django.urls import reverse
import os
from django.conf import settings


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
    trip_info = get_object_or_404(Trip, id=trip_id)
    trip_details = TripDetail.objects.filter(trip=trip_info)
    # expensedetail = ExpenseDetail.objects.filter(trip_detail=trip_details)

    if request.method == 'POST':

        ExpenseDetail.objects.filter(trip_detail__in=trip_details).delete()  
        expensedetails = {}

        for idx, trip_detail in enumerate(trip_details):
            memo_key = f'memo_{idx}'
            receipt_key = f'files_{idx}'
            memo = request.POST.get(memo_key)
            receipt = request.FILES.get(receipt_key)
            if memo or receipt:
                expensedetail = ExpenseDetail()
                expensedetail.trip_detail = trip_detail
                expensedetail.memo = memo

                if receipt:
                    expensedetail.receipt = receipt
                
                expensedetails[trip_detail.id] = expensedetail
                expensedetail.save()
                print(f"Saved: {expensedetail}")

        total_expense = sum(x.expense for x in trip_details)

        content = {
            'trip_info' : trip_info,
            'trip_details' : trip_details,
            'total_expense': total_expense,
            'trip_id':trip_id,
            'expensedetails':expensedetails,
        }
        return render(request, 'expense/index2.html', content)
    else:
        expensedetails = {td.id: ExpenseDetail.objects.filter(trip_detail=td).first()
                           for td in trip_details}
        if request.user.is_active:  
            total_expense = sum(x.expense for x in trip_details)
            content = {
                    'trip_info' : trip_info,
                    'trip_details' : trip_details,
                    'total_expense': total_expense,
                    'trip_id': trip_id,
                    'expensedetails': expensedetails,
                }
            return render(request, 'expense/index2.html', content);
        else:
            return HttpResponse("User is not active")
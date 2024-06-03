from django.core.files.storage import default_storage
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

    if request.method == 'POST':
        for idx, trip_detail in enumerate(trip_details):
            memo_key = f'memo_{idx}'
            receipt_key = f'files_{idx}'
            delete_key = f'delete_{idx}'

            memo = request.POST.get(memo_key)
            receipt = request.FILES.get(receipt_key)
            delete = request.POST.get(delete_key) == 'true'

            expensedetail, created = ExpenseDetail.objects.get_or_create(trip_detail=trip_detail)
            expensedetail.memo = memo

            # 파일이 새로 업로드된 경우 또는 삭제 요청이 있는 경우
            if receipt or delete:
                # 기존 파일 삭제
                if expensedetail.receipt and delete:
                    file_path = os.path.join(settings.MEDIA_ROOT, expensedetail.receipt.name)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                
                # 새 파일이 업로드된 경우에만 저장
                if receipt:
                    expensedetail.receipt = receipt
                else:
                    expensedetail.receipt = None

            expensedetail.save()
            
        total_expense = sum(x.expense for x in trip_details)

        content = {
            'trip_info': trip_info,
            'trip_details': trip_details,
            'total_expense': total_expense,
            'trip_id': trip_id,
            'expensedetails': {td.id: ExpenseDetail.objects.filter(trip_detail=td).first() for td in trip_details},
        }
        return render(request, 'expense/index2.html', content)
    else:
        expensedetails = {td.id: ExpenseDetail.objects.filter(trip_detail=td).first() for td in trip_details}
        if request.user.is_active:
            total_expense = sum(x.expense for x in trip_details)
            content = {
                'trip_info': trip_info,
                'trip_details': trip_details,
                'total_expense': total_expense,
                'trip_id': trip_id,
                'expensedetails': expensedetails,
            }
            return render(request, 'expense/index2.html', content)
        else:
            return HttpResponse("User is not active")



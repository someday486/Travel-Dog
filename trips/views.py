from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Region, Trip

@login_required
def index(request):
    if request.method == 'POST':
        region_id = request.POST.get('selected_region')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        region = Region.objects.get(id=region_id)
        Trip.objects.create(user=request.user, region=region, start_date=start_date, end_date=end_date)
        return redirect('/')  # 다음 페이지로 이동

    regions = Region.objects.all()
    return render(request, 'trips/index.html', {'regions': regions})

@login_required
def next_page(request):
    return render(request, '/')  # 다음 페이지 템플릿으로 이동
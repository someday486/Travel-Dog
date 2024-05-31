from django.shortcuts import render, HttpResponse
from myplace.models import Myplace
from trips.models import Destination



def myplace(request):
    if request.user.is_active:
        myplace = Myplace.objects.filter(user=request.user).select_related('destination')
        content = {
            'myplace': myplace,
            
        }
        print(myplace)
        return render(request,'destinations/myplace.html',content)
    
    else:
        msg = "<script>;"
        msg += "alert('로그인이 되어 있지 않습니다. 로그인 페이지로 넘어갑니다.');"
        msg += "location.href='/admin';"
        msg += "</script>;"
        return HttpResponse(msg)
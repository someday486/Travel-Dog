from django.shortcuts import render, HttpResponse
from myplace.models import Myplace
from trips.models import Destination, Trip
#사진 크롤링 관련 라이브러리
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.decorators import login_required

@login_required
def myplace(request):
    if request.user.is_active:
        print('myplace')
        myplace = Myplace.objects.filter(user=request.user).select_related('destination')
        # trip_id = Trip.objects.filter
        
        destinationSrc = []
        for i in myplace:
            destination_address = i.destination.address
            v = imgdown(destination_address)
            id = i.id               
            destinationSrc.append((i, v, id))

        content = {
            'destinationSrc': destinationSrc,
        }
        
        return render(request, 'destinations/myplace.html', content)
                       
    else:
        msg = "<script>;"
        msg += "alert('로그인이 되어 있지 않습니다. 로그인 페이지로 넘어갑니다.');"
        msg += "location.href='/admin';"
        msg += "</script>;"
        return HttpResponse(msg)
    
    
def imgdown(address):
    
    search_url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=" + address

    html = requests.get(search_url)

    # BeautifulSoup으로 파싱
    soup = BeautifulSoup(html.text, "html.parser")
    
    # # 이미지 태그 선택
    image_tags = soup.select(".img")
    # 이미지 소스 URL을 담을 리스트 생성
    src_list = []

    # # 이미지 태그의 src 속성을 src_list에 추가
    for img_tag in image_tags[2:3]:
        src = img_tag.get('src')
        src_list.append(src)
        
    return src_list

def delete(request):
    if request.method == 'POST':           
        destination_id = request.POST.get('destination_id') 
        myplace = Myplace.objects.filter(id=destination_id)
        myplace.delete()
        
        msg = "<script>;"
        msg += "alert('삭제되었습니다');"
        msg += "location.href='http://localhost:8000/myplace';"
        msg += "</script>;"
        return HttpResponse(msg)
    else:
        return render(request, 'destinations/myplace.html')
from django.shortcuts import render, HttpResponse, redirect
import json
import requests
# from bs4 import BeautifulSoup
import requests
from trips.models import Trip, Destination
import re


# Create your views here.

def location(request,trip_id):
    if request.method == 'GET':
        content = {
            'trip_id': trip_id,
        }
        return render(request, 'destinations/location.html',content)
    
    elif request.method == 'POST':
        url = "https://openapi.naver.com/v1/search/local.json"
        nheaders = {
            "X-Naver-Client-Id": "hhVJcqZEHfZM1cReFTCe",
            "X-Naver-Client-Secret": "l8jT5OgBQ8",
        }
        location = request.POST['location']
        param = {
            "query": location,
            "display" : 100,
            "start": 1,
            "sort": 'random',
        }

        res = requests.get(url, headers=nheaders, params=param)

        data = res.json()
        for item in data['items']:
            if 'title' in item:
                item['title'] = re.sub('<[^<]+?>|&amp;', '', item['title'])
        
        content = {
            'data': data['items'],
            'trip_id': trip_id,
        }

        return render(request, 'destinations/location.html', content)

def addtrip(request,trip_id,title,roadAdress):
    if request.method == 'POST':
        destination = Destination()
        destination.name = title
        destination.address = roadAdress
        destination.save()
        

        return redirect('trips:next_page')

def addmyplace(request,trip_id,title,roadAddress):
    if request.user.is_active: 
        
        if Destination.objects.filter(address=roadAddress):
            msg = "<script>;"
            msg += "alert('이미 저장되어 있는 장소입니다.');"
            msg += f"location.href='http://localhost:8000/destinations/{ trip_id }';"
            msg += "</script>;"
            return HttpResponse(msg)
        else:
            destination = Destination()
            destination.name = title
            destination.address = roadAddress
            destination.save()
            
            msg = "<script>;"
            msg += "alert('내장소에 추가 되었습니다.');"
            msg += f"location.href='http://localhost:8000/trips/next_page/{ trip_id }';"
            msg += "</script>;"
            return HttpResponse(msg)
    else:
        msg = "<script>;"
        msg += "alert('로그인이 되어 있지 않습니다. 로그인 페이지로 넘어갑니다.');"
        msg += "location.href='/admin';"
        msg += "</script>;"
        return HttpResponse(msg)
    
def myplace(request):
    if request.user.is_active:
        destination = Destination.objects.all()
        content = {
            'destination':destination,
        }
        return render(request,'destinations/myplace.html',content)
    
    else:
        msg = "<script>;"
        msg += "alert('로그인이 되어 있지 않습니다. 로그인 페이지로 넘어갑니다.');"
        msg += "location.href='/admin';"
        msg += "</script>;"
        return HttpResponse(msg)
    


def searchElse(request):
    url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query="

    keword = input('검색어입력: ')
    search_url = url + keword

    data = requests.get(search_url)
    # print(r.text[11000:15000])
    content = {
        'data' : data
    }
    return render(request, content)

    
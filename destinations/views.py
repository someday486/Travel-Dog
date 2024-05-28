from django.shortcuts import render
import json
import requests
# from bs4 import BeautifulSoup
import requests
from trips.models import Trip, Destination

# Create your views here.

def location(request):
    if request.method == 'GET':
        return render(request, 'destinations/location.html')
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
        content = {
            'data': data['items']
        }

        return render(request, 'destinations/location.html', content)


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

def addtrip(request,title,roadAdress):
    if request.method == 'POST':
        destination = Destination()       
        destination.name = title
        destination.address = roadAdress
        destination.save()
        return render(request, "trips/index.html")

    
from django.shortcuts import render
import json
import requests
# from bs4 import BeautifulSoup
import requests

# Create your views here.

def index(request):
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
            "display" : 10,
            "start": 6,
            "sort": 'random',
        }

        res = requests.get(url, headers=nheaders, params=param)

        data = res.json()
        print(data)
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
    
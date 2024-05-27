from django.shortcuts import render
import json  
import requests
from bs4 import BeautifulSoup
import requests

# Create your views here.

def index(request):
    return render(request, 'destinations/location.html')

def searchLocation(request):

    url = "https://openapi.naver.com/v1/search/local.json"  # API받아오기
    nheaders = {
        "X-Naver-Client-Id": "hhVJcqZEHfZM1cReFTCe",  #클라이언트 아이디/시크릿
        "X-Naver-Client-Secret": "l8jT5OgBQ8",
    }

    param = {
        "query": "홍대 맛집",
    }

    res = requests.get(url, headers=nheaders, params=param)

    # print(f"Status Code: {res.status_code}")
    # json.dumps(data, indent=4, ensure_ascii=False) #제이슨 파일

    # 요청 결과 출력
    data = res.json()
    data = json.loads(json.dumps(data, indent=4, ensure_ascii=False))
    content = {
        'data' : data
    }
    return render(request, content)


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
    
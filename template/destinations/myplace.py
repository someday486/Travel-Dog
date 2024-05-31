from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query="

keword = "제주특별자치도 서귀포시 성산읍 섭지코지로 95 아쿠아플라넷 제주"
search_url = url + keword

# Chrome WebDriver 옵션 설정
options = Options()
options.add_argument('--headless')  # 브라우저 숨기기

# Chrome WebDriver 생성
driver = webdriver.Chrome(options=options)

# 블로그 페이지 열기
driver.get(search_url)

# 페이지 소스 가져오기
html = driver.page_source

# BeautifulSoup으로 파싱
soup = BeautifulSoup(html, "html.parser")

# 이미지 태그 선택
image_tags = soup.find_all("img")

# 이미지 소스 URL을 담을 리스트 생성
src_list = []

# 이미지 태그의 src 속성을 src_list에 추가
for img_tag in image_tags[2:12]:
    src = img_tag.get('src')
    src_list.append(src)

print(src_list)
    
# 웹 브라우저 닫기
driver.quit()

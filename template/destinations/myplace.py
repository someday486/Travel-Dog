from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

base_url = "https://map.naver.com/p/search/"

keyword = "제주특별자치도 서귀포시 성산읍 섭지코지로 95 아쿠아플라넷 제주"

search_url = base_url + keyword

r = requests.get(search_url)

print(r.text)



# driver = webdriver.Chrome()

# css = '#app-root > div > div > div > div.CB8aP > div > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div > a > img src'  # 사진의 CSS 셀렉터
# try:
#     # 페이지 열기
#     driver.get(search_url)
#     print("페이지 로드 중...")

#     # 사진 섹션이 로드될 때까지 대기
#     WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, css))
#     )
#     print("페이지 로드 완료")

#     # 사진 요소 찾기
#     images = driver.find_elements(By.CSS_SELECTOR, css)
    
#     # 이미지 URL 추출 및 출력
#     print(f"사진 수: {len(images)}")
#     for i, img in enumerate(images, 1):
#         print(f'{i}: {img.get_attribute("src")}')
# finally:
#     # 드라이버 종료
#     driver.quit()
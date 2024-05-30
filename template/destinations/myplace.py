from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

base_url = "https://map.naver.com/p/search/"

keyword = input('검색어: ')

search_url = base_url + keyword
driver = webdriver.Chrome()
css = '#_pcmap_list_scroll_container > ul > li:nth-child(4) > div.cOfu6.FlUUg.bnOAZ > div > div > div > div:nth-child(1) > a'
try:
    # 검색 페이지로 이동
    driver.get(search_url)
    print("페이지 로드 중...")

    # 페이지가 로드될 때까지 기다림
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css))
    )
    print("페이지 로드 완료")

    # 페이지 소스 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    
    # 검색 결과 선택
    items = soup.select(css)
    print(f"검색 결과 수: {len(items)}")

    for i, v in enumerate(items, 1):
        print(f'{i}: {v.text.strip()}')

finally:
    # 드라이버 종료
    driver.quit()

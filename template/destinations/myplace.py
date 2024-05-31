from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests



url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query="

keword = "제주특별자치도 서귀포시 성산읍 섭지코지로 95 아쿠아플라넷 제주"
search_url = url + keword
# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Open the search URL
    driver.get(search_url)
   
    # Wait until images are loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "img"))
    )
   
    # Find all image elements
    images = driver.find_elements(By.TAG_NAME, "img")
   
    # Extract the source URLs of the images
    img_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]

    # Download the images
    for idx, img_url in enumerate(img_urls):
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(f"image_{idx}.jpg", "wb") as file:
                file.write(response.content)
            print(f"Downloaded image_{idx}.jpg")
        else:
            print(f"Failed to download image from {img_url}")

finally:
    # Close the WebDriver
    driver.quit()
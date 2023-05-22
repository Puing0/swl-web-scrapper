from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\dell\\OneDrive\\Desktop\\PFE MASTER\\chromedriver.exe"

wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def get_images_url(wd, delay):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)
	url = "https://www.spaceweatherlive.com/fr/archives/2023/05/01/dayobs.html"
	wd.get(url)

	image_urls = set()
	skips = 0

	scroll_down(wd)
	images = wd.find_elements(By.CSS_SELECTOR, '[alt="HMIIF"]')
	classes = wd.find_elements(By.CLASS_NAME, 'region_mag')
	for image in images:
		if image.get_attribute('src') :
			image_urls.add(image.get_attribute('src'))
			print(f"Found {len(image_urls)}")

	return image_urls



def download_image(download_path, url, file_name):
	try:
		agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36\
		(KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		image_content = requests.get(url, headers={'User-Agent': agent})
		image_content.raise_for_status()
		# image = Image.open(io.BytesIO(image_content.content))
		
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			print("im here")
			f.write(image_content.content)

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_url(wd, 2)
print(urls)

for i, url in enumerate(urls):
	download_image("imgs/", url, str(i) + ".jpg")

wd.quit()

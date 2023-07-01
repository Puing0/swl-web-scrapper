import requests
# import io
# from PIL import Image
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_images_url(wd, delay):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    scroll_down(wd)

    images = wd.find_elements(By.CSS_SELECTOR, '[alt="HMIBC"]')
    labels = wd.find_elements(By.CLASS_NAME, 'region_mag')

    image_urls = []
    label_classes = []

    for image in images:
        if image.get_attribute('src'):
            image_urls.append(image.get_attribute('src'))
    
    for label in labels:
        class_name = label.get_attribute('class')
        label_classes.append(class_name[11:])
    
    return image_urls, label_classes

def download_image(download_path, url, file_name):
    try:
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        headers = {'User-Agent': agent}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        file_path = download_path + file_name

        with open(file_path, "wb") as file:
            file.write(response.content)

        # print("Image downloaded successfully:", file_path)
    except Exception as e:
        print('FAILED -', e)

def navigate_to_next_page(wd):
    anchor_point = wd.find_elements(By.XPATH, "//a[.//span[text()='Jour prochain']]")[0]
    wd.execute_script("arguments[0].click();", anchor_point) 
    print(wd.current_url)

# Set up the WebDriver
wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the initial URL
url = "https://www.spaceweatherlive.com/fr/archives/2022/01/01/dayobs.html"
wd.get(url)

# Variables for image count and delay
j = 0
delay = 2

# Main loop to navigate, extract image URLs, and download images
alpha_idx = 0
beta_idx = 0
betax_idx = 0
while j < 3000:
    try:
        image_urls, labels = get_images_url(wd, delay)
        # print("image size url and labels: "+ len(image_urls)+" "+ len(labels))
        for i, url in enumerate(image_urls):
            label = labels[i]
            yy = url[49:53]
            mm = url[54:56]
            dd = url[57:59]
            date  = yy+"-"+mm+"-"+dd

            if label == 'A':
                download_image("imgs/alpha/", url, date+"_"+str(alpha_idx) + ".jpg")
                alpha_idx+=1
            elif label == 'B':
                download_image("imgs/beta/", url, date+"_"+str(beta_idx) + ".jpg")
                beta_idx+=1
            else:
                download_image("imgs/betax/", url, date+"_"+str(betax_idx) + ".jpg")
                betax_idx+=1
            
            j += 1

        navigate_to_next_page(wd)
        time.sleep(10)
    except Exception as e:
        print('Error:', e)
        break

# Quit the WebDriver
wd.quit()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import requests
import time
import pandas as pd

def product_page(code):   
    url = "https://www2.hm.com/en_my/productpage.%s.html" % str(code)
    return url

def extract_image(code):
    image_tag = driver.find_elements(By.XPATH,"//div[@class='product-detail-main-image-container']/img")
    main_img_url = [img.get_attribute('src') for img in image_tag]
    if len(main_img_url) > 0:
       main_img_data = requests.get(main_img_url[0]).content
    else: 
       return
    with open(str(code) + "/img1.jpg", 'wb') as f: 
            f.write(main_img_data)
    
    image_secondary_tags = driver.find_elements(By.XPATH,"//img[@class='product-detail-thumbnail-image']")
    url_list = [img.get_attribute('src') for img in image_secondary_tags]
    if len(url_list) > 0:
        for i in url_list:
            images_url = 'https:' + i
            img_data = requests.get(images_url).content
            with open(str(code) + "/img%s.jpg" % str(url_list.index(i)+2), 'wb') as f: 
                f.write(img_data)
    else:
        return
    
def extract_video(code) :
    video_tag = driver.find_elements(By.XPATH,"//video[@class='vjs-tech']")
    video_url = [video.get_attribute('src') for video in video_tag]
    if len(video_url) > 0:
        for i in video_url:
            vid_data = requests.get(i).content
            with open(str(code) + "/video%s.mp4" % str(video_url.index(i)+1), 'wb') as v: 
                v.write(vid_data)
    else:
        return


data = pd.read_excel(r'c:\users\leona\Question_1_Dataset.xlsx')
df = pd.DataFrame(data, columns=['Article Number'])
df = df.dropna()
df = df.astype(int).astype(str)
df['Article Number'] = df['Article Number'].str.zfill(10)
product_list = df['Article Number'].values.tolist()

for product_code in product_list:
    path = os.path.join("C:/Users/leona/", "%s" % str(product_code))
    if os.path.exists(path):
        continue
    os.mkdir(path)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(product_page(product_code))
    time.sleep(6)
    extract_image(product_code)
    extract_video(product_code)
    driver.close








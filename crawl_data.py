from requests.api import get
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox import options
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import  random
from urllib.request import urlretrieve
import requests
import os

PATH = r"D:\CrawlData\geckodriver.exe"
EDGPATH = r"D:\EdgDriver\msedgedriver.exe"
COUNT = 0
SOURCR_IMAGE_URLs = []
SOURCE = []
options = webdriver.FirefoxOptions()
options.add_argument('--no-sandbox')


driver = webdriver.Firefox(executable_path=PATH, options=options)
# driver = webdriver.Edge(executable_path=EDGPATH) 
action = ActionChains(driver)


def get_all_result(search_url,dirs):
    driver.get(search_url)
    print(driver.title)

    # scroll to end page
    element = driver.find_element(By.TAG_NAME,value='body')
    for i in range(250):
        print(i, end="\a")
        time.sleep(random.randrange(4))
        element.send_keys(Keys.PAGE_DOWN)
        try:
            more_result = WebDriverWait(driver,1).until(
                EC.presence_of_element_located((By.CLASS_NAME,"infinite-scroll-load-more"))
            )
            more_result.click()
            print("clicked!")
            time.sleep(5)
            # for j in range(100):
            #     element.send_keys(Keys.PAGE_DOWN)
        except Exception as error:
            print(error, end="\a")        
            continue

    print('end page')
    time.sleep(0.5)

    count = 0 
    tag_a = driver.find_elements(By.TAG_NAME, value='a')
    for a in tag_a:
        if a.get_attribute("class") == "overlay":
            SOURCE.append(a.get_attribute("href"))
    print(len(SOURCE))        
    all_result = driver.find_elements(By.CLASS_NAME, value="overlay")
    print(len(all_result))
    for result in all_result:
        source_image_url = result.get_attribute("href")
        print(source_image_url)
        SOURCR_IMAGE_URLs.append(source_image_url)
        count += 1

    print(count)
    # driver.quit()
    download_image(dirs)
    

def download_image(dirs):
    for source_url in SOURCR_IMAGE_URLs:
        print(source_url)
        driver.get(source_url)
        try:
            image = WebDriverWait(driver,2).until(
                EC.presence_of_element_located((By.CLASS_NAME,"main-photo"))
            )
            image_url = image.get_attribute("src")
            print(image_url)
            res = requests.get(image_url, verify=True, stream=True)
            rawdata = res.raw.read()
            file_name = image_url.split("?")[0].split("/")[-1]
            # dirs = "Trafic"
            if not os.path.exists(dirs):
                os.makedirs(dirs)
            with open(os.path.join(dirs,file_name), 'wb') as f:
                f.write(rawdata)
        except Exception as e:
            print('Failed to write rawdata.')
            print(e)


def main():
    get_all_result("https://www.flickr.com/search/?media=photos&text=family","Family")
    get_all_result("https://www.flickr.com/search/?text=trafic&media=photos","Tracfic")
    get_all_result("https://www.flickr.com/search/?media=photos&advanced=1&text=student","Student")
    get_all_result("https://www.flickr.com/search/?media=photos&advanced=1&text=traffic%20accidents","Tracffic_accidents")
    get_all_result("https://www.flickr.com/search/?media=photos&advanced=1&text=school","School")
    get_all_result("https://www.flickr.com/search/?media=photos&advanced=1&text=domestic%20violence","Domestic_violence")


 


if __name__ == '__main__':
    main()

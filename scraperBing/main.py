from logging import log
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import requests
import os


def clean():
    if os.path.exists('./out'):
        for f in os.listdir('./out'):
            os.remove(os.path.join('./out', f))


def scrape(category, scrolls=5):
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    s = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    driver.get(f'https://www.bing.com/images/search?q={category}')

    added_pictures = 0

    for i in range(scrolls):
        driver.execute_script(
            "window.scrollTo(0,document.body.scrollHeight)")

        try:
            loadMoreButton = driver.find_element_by_xpath(
                "//a[text()='See more images' or text()='Meer afbeeldingen weergeven']")
            loadMoreButton.click()
        except:
            print("No button to press")

        print('Loaded more photos')
        time.sleep(1)

    images = driver.find_elements_by_xpath("//img[contains(@class, 'mimg')]")

    for img in images:
        source = img.get_attribute("src")
        
        if "https://th.bing.com" in source:
            img_data = requests.get(source).content

            with open(f'./out/{category}-{added_pictures}.jpg', 'wb') as handler:
                handler.write(img_data)
                added_pictures += 1

    print(f"Download pictures")


fruits = ['banana fruit', 'avocado', 'apple fruit', 'orange fruit', 'grape']

clean()
for fruit in fruits:
    scrape(fruit, 5)

from selenium import webdriver, common
from selenium.webdriver.common.keys import Keys
import time, os, json
from PIL import Image
import pandas as pd
from pprint import pprint
import base64
from lib.parse import parse_captcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from lib.upload import uploader
from lib.DA_opener import open_DA
CAPTCHA_DIM = (180, 45)
CHARACTER_DIM = (30, 32)
FPATH = os.path.dirname(os.path.realpath(__file__))

driver = webdriver.Edge('assets/msedgedriver.exe')
driver.get("https://vtop.vit.ac.in/vtop/initialProcess")

def escape_timeout_page(driver):
    driver.refresh()
    driver.find_element_by_xpath("//*[@id='closedHTML']/div/div/div/div[2]/div/div/a").click()
    time.sleep(1)
    driver.find_element_by_xpath("//*[@id='page-wrapper']/div/div[1]/div[1]/div[3]/div/button").click()

def fill_form(driver,uname, passwd):
    driver.find_element_by_xpath("//*[@id='uname']").send_keys(uname)
    driver.find_element_by_name("passwd").send_keys(passwd)
    time.sleep(1)
    _,img_data = driver.find_element_by_xpath("//*[@id='captchaRefresh']/div/img").get_attribute("src").split(' ')
    img_data = base64.b64decode(img_data)
    img_name = 'assets/captcha.png'
    with open(img_name, 'wb') as f:
        f.write(img_data)
    ocr_result = parse_captcha(Image.open(os.path.join(FPATH, "captcha.png")))
    print(ocr_result)
    driver.find_element_by_xpath("//*[@id='captchaCheck']").send_keys(ocr_result)
    driver.find_element_by_xpath("//*[@id='captcha']").click()


def check_login_success(driver):
    while 'value="19BCE0984"' not in driver.page_source:
        try:
            fill_form(driver,os.getenv('USERNAME'), os.getenv('PASSWORD'))
            return False
        except:
            print("RELOAD")
            return True
        

repeat = False
while True:
    escape_timeout_page(driver)
    time.sleep(2)
    repeat  = check_login_success(driver)
    if repeat:
        continue
    else:
        break
time.sleep(2)
DA_list = open_DA(driver)

choice = int(input("Kaunsa DA submit karoge? (Choose index no.): "))
ret = uploader(driver, DA_list[choice-1][1])

'''
select = driver.find_element_by_xpath("//*[@id='semesterSubId']/option[3]")
print(select)
for option in select.options:
    print(option)
    #print(option.text, option.get_attribute('value'))


# driver.close() # Closes currently focused browser
#driver.quit() # Closes all tabs of browser
'''
from selenium import webdriver, common
import os, sys
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
import time, os, json
from PIL import Image
from getpass import getpass
import pandas as pd
import base64
from lib.parser import parse_captcha
from lib.upload import uploader
from lib.DA_opener import open_DA
from dotenv import load_dotenv


CAPTCHA_DIM = (180, 45)
CHARACTER_DIM = (30, 32)
if getattr(sys, 'frozen', False):
    FPATH = os.path.dirname(sys.executable)
elif __file__:
    FPATH = os.path.dirname(os.path.realpath(__file__))



CHROMEDRIVER_PATH = os.path.join(FPATH,'assets/chromedriver.exe')
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('log-level=3')
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

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
    img_name = os.path.join(FPATH,'assets/captcha.png')
    with open(img_name, 'wb') as f:
        f.write(img_data)
    ocr_result = parse_captcha(Image.open( img_name))
    print(ocr_result)
    driver.find_element_by_xpath("//*[@id='captchaCheck']").send_keys(ocr_result)
    driver.find_element_by_xpath("//*[@id='captcha']").click()


def check_login_success(driver):
    if os.path.exists('.env')==False:
        print("Enter your credentials for future use!")
        with open(os.path.join(FPATH,'.env'), 'w+') as f:
            user = "USER="+input("Enter Registration No.: ").upper()
            passwd = "PASS="+getpass()
            f.write(user+"\n"+passwd)
            time.sleep(1)
    load_dotenv()
    while 'value="'+os.getenv('USER')+'"' not in driver.page_source:
        try:
            fill_form(driver,os.getenv('USER'), os.getenv('PASS'))
            return False
        except:
            print("RELOAD")
            time.sleep(1)
            return True

if __name__=="__main__":
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
    uploader(driver, DA_list[choice-1][1])

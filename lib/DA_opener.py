import time
import pandas as pd
from selenium.webdriver.support.ui import Select, WebDriverWait
def open_DA(driver):
    driver.execute_script("javascript:loadmydiv('examinations/StudentDA')")
    time.sleep(3)
    drp = Select(driver.find_element_by_id("semesterSubId"))
    drp.select_by_visible_text("Winter Semester 2020-21")
    time.sleep(1)
    rows = len(driver.find_elements_by_xpath("//*[@id='fixedTableContainer']/table/tbody/tr"))
    cols = len(driver.find_elements_by_xpath("//*[@id='fixedTableContainer']/table/tbody/tr[2]/td"))
    print(rows, cols)
    data = [['' for i in range(cols)] for j in range(rows-1)]
    for r in range(2, rows+1):
        for c in range(1, cols):
            value = driver.find_element_by_xpath("//*[@id='fixedTableContainer']/table/tbody/tr["+str(r)+"]/td["+str(c)+"]").text
            data[r-2][c-1] = value
    
    for row in data:
        for i in range(len(row)):
            if i in [0,2,3,4]:
                print("{:40}".format(row[i]), end = ' ')
        print()
    return data
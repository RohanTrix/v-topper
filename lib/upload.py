import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time
from datetime import date, datetime
import tkinter as tk
from tkinter import filedialog
def click_button():
    def UploadAction(event=None):
        filename = filedialog.askopenfilename()
        with open('assets/filepath.txt', 'w+') as f:
            f.write(filename)
        root.destroy()
        return
    root = tk.Tk()
    button = tk.Button(root, text='Choose Assignment File', command=UploadAction)
    button.pack()
    root.mainloop()

def uploader(driver, class_nbr):
    cmd = "myFunction('"+class_nbr+"');"
    driver.execute_script(cmd)
    try:
        time.sleep(1)
        with open('assets/temp.html', 'w+') as f:
            f.write(driver.page_source)
        df = pd.read_html('assets/temp.html', header = 1, index_col = 0) 
        print(df[1])
        choice = input('Select DA no. to submit: ')
        assignment = "AST0"+str(choice)
        cmd = "//*[@id='fixedTableContainer']/table/tbody[2]/tr["+str(choice)+"]/td[8]/span/span/span/button/span"
        driver.find_element_by_xpath(cmd).click()
        click_button()
        file_path = open('assets/filepath.txt').read()
        driver.find_element_by_id('studDaUpload').send_keys(file_path)
        time.sleep(1)
        driver.find_element_by_xpath("//*[@id='myModal']/div/div/div[3]/button[1]").click()
        driver.execute_script("doSaveDigitalAssignment('"+class_nbr+"','"+assignment+"');")
    except:
        print("Some error Occured! Please try again")
        return
    time.sleep(2)
    if "Uploaded successfully" in driver.page_source:
        print("SUCESS!")
        return
    try:
        otp = driver.find_element_by_id("otpEmail")
        while True:
            otp.send_keys(input("Enter OTP: "))
            driver.find_element_by_xpath("//*[@id='daUploadOtpAlert']/div/div[5]/button").click()
            time.sleep(3)
            if "Uploaded successfully" in driver.page_source:
                print("SUCESS!")
                break
            print("WRONG OTP!")
    except NoSuchElementException:
        print("Someting Went Wrong!! Try Again")
        return
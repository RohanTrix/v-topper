import pandas as pd
import time
def uploader(driver, class_nbr):
    cmd = "myFunction('"+class_nbr+"');"
    driver.execute_script(cmd)
    time.sleep(1)

    

    
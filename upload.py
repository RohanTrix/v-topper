import pandas as pd
import time
def uploader(driver, class_nbr):
    cmd = "myFunction('"+class_nbr+"');"
    driver.execute_script(cmd)
    time.sleep(1)
    with open('temp.html', 'w+') as f:
        f.write(driver.page_source)
    df = pd.read_html('temp.html', header = 1, index_col = 0)
    
    #print(df[1].iloc[1:,0:7])
    

    
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import os
import datetime

def extract_code_KHLCNT(code):
    parts = code.split(":")

    if len(parts)>1:
        return parts[1].strip()
    else:
        return ""
    
def check_create_csv(filename,df):
    if os.path.exists(filename):
        os.remove(filename)
        print(f"Deleted file: {filename}")
    df.to_csv(filename,index=False)
    print(f"Created file: {filename}")


driver = webdriver.Firefox()

driver.get("https://muasamcong.mpi.gov.vn/web/guest/")
driver.maximize_window()

title = driver.title

driver.implicitly_wait(0.5)
#element = WebDriverWait(driver, 10000).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div/button/span')))

#element.click()
x_popup = driver.find_element(by=By.ID,value="popup-close")
x_popup.click()
#WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "bi bi-x"))).click()

radio1 = driver.find_element(by=By.ID, value="radio-1")
driver.execute_script("arguments[0].setAttribute('checked', 'checked')", radio1)
#radio1.click()

#clicking here makes sense
radio_khlcnt =  driver.find_element(By.CSS_SELECTOR,".check-box-parent > div:nth-child(2)")
radio_khlcnt.click()

#radio_khlcnt = driver.find_element(by=By.ID,value="radio-khlcnt")
#driver.execute_script("arguments[0].setAttribute('checked', 'checked')", radio_khlcnt)
#radio_khlcnt.click()

#radio_tbmt = driver.find_element(by=By.ID,value="radio-tbmt")
#driver.execute_script("arguments[0].removeAttribute('checked')", radio_tbmt)
#radio_tbmt.click()



investorChecked = driver.find_element(By.CSS_SELECTOR,"div.content__search__item:nth-child(3) > input:nth-child(1)")
investorChecked.click()

#text_box = driver.find_element(by=By.NAME, value="my-text")
search_box = driver.find_element(by=By.NAME,value="keyword")
f=open("test.txt","r",encoding="utf8")
search_box.send_keys(f.read())

submit_button = driver.find_element(by=By.CLASS_NAME, value="search-button")

submit_button.click()

driver.implicitly_wait(2.5) #wait for content to load

is_enabled = True
code_KHLCNT = {}

while is_enabled == True:
    time.sleep(2)
    #p_code = driver.find_elements(By.CLASS_NAME,"content__body__left__item__infor__code")
    # Wait for the elements to be present and visible
    p_code = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "content__body__left__item__infor__code"))
    )
    p_approved_date = []
    for elem in driver.find_elements(By.CLASS_NAME,"content__body__right__item__infor__contract"):
        p_approved_date.append(elem.find_element(By.TAG_NAME,"h5").text)
    
    for k,v in zip(p_code,p_approved_date):
        try:
            code_KHLCNT[(extract_code_KHLCNT(k.text))] = v
        except StaleElementReferenceException:
            #re-find
            print("Stale element encountered, skipping...")
            

    print(len(code_KHLCNT))


    try:

        next_btn = driver.find_element(By.CLASS_NAME,"btn-next")

        is_enabled = next_btn.is_enabled()

        next_btn.click()

    except StaleElementReferenceException:

        #re-initialize the element

        next_btn = driver.find_element(By.CLASS_NAME,"btn-next")

        is_enabled = next_btn.is_enabled()

        next_btn.click()

    finally:

        driver.implicitly_wait(20) #wait for content to load

#filter time
filtered_code_by_time = {key: value for key, value in code_KHLCNT.items() if datetime.datetime.strptime(value,"%d/%m/%Y") > datetime.datetime.strptime("01/07/2024","%d/%m/%Y")}
print(len(filtered_code_by_time))

#loop through code_KHLCNT and collect data
if len(filtered_code_by_time)>0:
    #get current window's handle
    original_window = driver.current_window_handle
    wait = WebDriverWait(driver,10)
    list_of_plans = []
    for code in filtered_code_by_time.keys():
        try:
            driver.implicitly_wait(2.5) #wait for content to load
            search_box = driver.find_element(by=By.NAME,value="keyword")
            search_box.clear()
            search_box.send_keys(code)
            submit_button = driver.find_element(by=By.CLASS_NAME, value="button__search")
            submit_button.click()
            driver.implicitly_wait(5) #wait for content to load
            time.sleep(3)
            
            link=driver.find_element(By.CSS_SELECTOR,"div.content__body__left__item:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > a:nth-child(1) > h5:nth-child(1)")
            # create action chain object
            action = ActionChains(driver)
            #action.click(link).perform()
            action.move_to_element(link).key_down(Keys.COMMAND).click(link).key_up(Keys.COMMAND).perform()
            driver.implicitly_wait(10) #wait for content to load
            time.sleep(8)

            
            table_body = driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/section/div/div/div/div/section/div/div[2]/div/div/div[2]/main/div/div/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody")
            #table_body = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(By.XPATH,"/html/body/div[1]/div[1]/section/div/div/div/div/section/div/div[2]/div/div/div[2]/main/div/div/div[1]/div[2]/div[1]/div[5]/div[2]/table/tbody"))

            
            for row in table_body.find_elements(By.TAG_NAME,"tr"): 
                sub_plan = []        
                cells = row.find_elements(By.TAG_NAME,"td")
                for i in range(1,len(cells)): #skip the first td
                    if (cells[i].text!=""): #skip Giam sat hoat dong nha thau (neu co)
                        sub_plan.append(cells[i].text)
                list_of_plans.append(sub_plan)
            print(len(list_of_plans))

            #close and switch back
            driver.back()
        except Exception:
            continue

driver.quit()

if len(list_of_plans)>0:
    df = pd.DataFrame(list_of_plans)
    check_create_csv("ContractorPlan.csv",df)



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def extract_code_KHLCNT(code):
    parts = code.split(":")

    if len(parts)>1:
        return parts[1].strip()
    else:
        return ""

driver = webdriver.Firefox()

driver.get("https://muasamcong.mpi.gov.vn/web/guest/")

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
code_KHLCNT = []

while is_enabled == True:
    time.sleep(5)
    #p_code = driver.find_elements(By.CLASS_NAME,"content__body__left__item__infor__code")
    # Wait for the elements to be present and visible
    p_code = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CLASS_NAME, "content__body__left__item__infor__code"))
    )
    
    for item in p_code:
        try:
            code_KHLCNT.append(extract_code_KHLCNT(item.text))
        except StaleElementReferenceException:
            #re-find
            print("Stale element encountered, skipping...")
            

    print(len(code_KHLCNT))

    # # Wait for the button to be visible and clickable
    # next_btn = WebDriverWait(driver, 20).until(
    #     EC.visibility_of_element_located((By.CLASS_NAME, "btn-next"))
    # )

    # is_enabled = next_btn.is_enabled()

    # # Check if the button is enabled
    # if next_btn.is_enabled():
    #     # Click the button
    #     next_btn.click()    

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


print(len(code_KHLCNT))

#loop through code_KHLCNT and collect data


driver.quit()

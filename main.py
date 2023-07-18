import selenium
from selenium import webdriver
# from bs4 import BeautifulSoup
import time

from selenium.webdriver.common.by import By

browser = webdriver.Chrome(executable_path="./chromedriver.exe")

URL = 'https://carrier.superdispatch.com/tms/loads'
LOGIN = "empire120@gmail.com"
PASSWORD = "vito1212"

browser.maximize_window()
browser.get(URL)
# time.sleep(600)

login_input = browser.find_element(By.ID, "uid_1")
login_input.clear()
login_input.send_keys(LOGIN)

pass_input = browser.find_element(By.ID, "uid_2")
pass_input.clear()
pass_input.send_keys(PASSWORD)

btn_sign = browser.find_element(By.XPATH, r"/html/body/div[1]/div/div[1]/div/div/div/form/div/div[2]/button")
btn_sign.click()
time.sleep(2)


# class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-1" # sheet of loads

# class="Stack__StackRoot-SD__sc-qkml7c-0 dtlYiC"


loads = browser.find_element(By.CLASS_NAME, "Stack__StackRoot-SD__sc-qkml7c-0 dtlYiC")
print(loads)

# print(browser.page_source)

# load_name_list = browser.find_elements(By.CLASS_NAME, "MuiCardContent-root")
# print(load_name_list)
# print(len(load_name_list))

time.sleep(600)


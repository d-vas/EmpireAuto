import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from settings import ONE_DISP

URL = 'https://www.1dispatch.com/Carrier/CarrierViewHistory?DataType=ReLoad'


def one_disp_login_getting_table(login, password, url):
    browser = webdriver.Chrome()
    browser.get(url)
    if browser.find_element(By.CLASS_NAME, "formdisplay"):
        browser.find_element(By.ID, "UserName").send_keys(login)
        browser.find_element(By.ID, "Password").send_keys(password)
        browser.find_element(By.ID, "btnLogin").click()


'''
    # show_all
    select_element = Select(browser.find_element(By.CLASS_NAME, "ui-multiselect ui-widget ui-state-default ui-corner-all carrier-my-load-filter"))
    select_element.select_by_visible_text("All")


    # get_table
    tables = browser.find_elements(By.CSS_SELECTOR, "table") #res list of selenium elements
    table = tables[2] #res - sel elem
    table_html = table.get_attribute('outerHTML') #res - html-str
    return table_html
'''


one_disp_login_getting_table(ONE_DISP['login'], ONE_DISP['pass'], url=URL)


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import settings
from io import StringIO


URL = 'https://www.1dispatch.com/Carrier/CarrierViewHistory?DataType=ReLoad'
login = settings.ONE_DISP['login']
password = settings.ONE_DISP['password']

def one_disp_login_getting_table(login, password, url):
    browser = webdriver.Chrome()
    browser.get(url)
    if browser.find_element(By.CLASS_NAME, "formdisplay"):
        browser.find_element(By.ID, "UserName").send_keys(login)
        browser.find_element(By.ID, "Password").send_keys(password)
        browser.find_element(By.ID, "btnLogin").click()
    browser.find_elements(By.ID, "CarrierViewHistory_Menu")[1].click()

    browser.find_element(By.CLASS_NAME, "ui-multiselect ui-widget ui-state-default ui-corner-all carrier-my-load-filter").click()



    checkbox_ppu = browser.find_element(By.CLASS_NAME, "ui-corner-all ui-state-hover")
    if not checkbox_ppu.is_selected():
        checkbox_ppu.click()
    checkbox_pdel = browser.find_element(By.CLASS_NAME, "ui-corner-all")
    if not checkbox_pdel.is_selected():
        checkbox_pdel.click()

    table = browser.find_element(By.ID, "ajaxPanel1")
    # print(table)
    # print(type(table))
    table_html = table.get_attribute('outerHTML')
    # print(table_html)
    html_io = StringIO(table_html)
    # df = pd.read_html(table_html)[0]
    df = pd.read_html(html_io)
    # df = df.iloc[:, 3:]
    print(df)


    #
    # WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, "admin_auctions")))
    #
    # browser.find_element(By.ID, "btnFilterStatus").click()



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


one_disp_login_getting_table(login, password, url=URL)


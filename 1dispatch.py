import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import settings
from io import StringIO
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


URL = 'https://www.1dispatch.com/Carrier/CarrierViewHistory?DataType=ReLoad'
login = settings.ONE_DISP['login']
password = settings.ONE_DISP['password']
URL_DASH = 'https://www.1dispatch.com/Carrier/CarrierDashboard'

path_to_chromedriver = r"C:\chromedriver.exe"
service = webdriver.chrome.service.Service(path_to_chromedriver)
webdriver.chrome.service.Service.DEFAULT_CHROME_ARGS = ["--disable-extensions"]
webdriver.chrome.service.Service.DEFAULT_CHROME_BINARY_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# browser = webdriver.Chrome()
browser = webdriver.Chrome(service=service, ex)

# browser = webdriver.Chrome(executable_path="C:\chromedriver.exe")


def one_disp_login(login, password, url, browser):
    browser.get(url)
    if browser.find_element(By.CLASS_NAME, "formdisplay"):
        browser.find_element(By.ID, "UserName").send_keys(login)
        browser.find_element(By.ID, "Password").send_keys(password)
        browser.find_element(By.ID, "btnLogin").click()


def getting_all_table(login, password, url, browser):
    one_disp_login(login, password, URL, browser)

    '''    # tbl = browser.find_element(By.ID, 'carrier_dashboard')
    tbl = browser.find_elements(By.ID, 'ajaxPanel1')
    print(len(tbl))
    print(tbl.text)'''

    '''list_of_elements = browser.find_elements(By.ID, "CarrierViewHistory_Menu")
    print(list_of_elements[-1].text)'''
    # whole_table = browser.find_element(By.ID, 'admin_auctions')
    # print(whole_table)
    '''    list_of_elements = browser.find_elements(By.TAG_NAME, 'table')
    print(len(list_of_elements))'''
    browser.find_elements(By.ID, 'CarrierViewHistory_Menu')[-1].click()
    tbl1 = browser.find_element(By.ID, 'admin_auctions')
    # print(tbl1.text)
    list_of_loads = tbl1.find_elements(By.CLASS_NAME, 't-last')

    # list_of_elements = browser.find_elements(By.CLASS_NAME, "ui-multiselect ui-widget ui-state-default ui-corner-all carrier-my-load-filter")
    # print(list_of_elements)

    # browser.find_element(By.CLASS_NAME, "ui-icon ui-icon-triangle-2-n-s").click()

    # hidden_element = browser.find_element(By.CLASS_NAME, "ui-multiselect-menu ui-widget ui-widget-content ui-corner-all carrier-my-load-filter")
    # browser.execute_script("arguments[0].style.display = 'block';", hidden_element)

    # class ="ui-multiselect-menu ui-widget ui-widget-content ui-corner-all carrier-my-load-filter"

    # browser.find_element(By.ID, 'ui - multiselect - filterStatus - option - 1').click()
    # browser.find_element(By.ID, 'ui - multiselect - filterStatus - option - 2').click()

    # checkbox_ppu = browser.find_element(By.CLASS_NAME, "ui-corner-all ui-state-hover")
    # if not checkbox_ppu.is_selected():
    #     checkbox_ppu.click()
    # checkbox_pdel = browser.find_element(By.CLASS_NAME, "ui-corner-all")
    # if not checkbox_pdel.is_selected():
    #     checkbox_pdel.click()
    # element = WebDriverWait(browser, 10).until(
    #     EC.visibility_of_element_located((By.ID, "your_element_id"))
    # )

    '''wait = WebDriverWait(browser, 10)
    element = wait.until(EC.visibility_of_element_located((By.ID, "per_page_count")))'''

    '''    select_element = Select(browser.find_element(By.ID, "perpage"))
    select_element.select_by_visible_text("All")'''




    count_of_loads = browser.find_element(By.ID, "per_page_count").click()
    list_of_options = browser.find_elements(By.CLASS_NAME, "t-animation-container")
    list_of_options[-1].find_elements(By.CLASS_NAME, 't-item')[-1].click()
    # print(len(list_of_options))
    # print(count_of_loads.text)
    # input_field = count_of_loads.find_element(By.CLASS_NAME, 't-input')
    # input_field.send_keys("200")
    # count_of_loads.find_element(By.ID, 'hdnEventPerPage').send_keys('200')
    # element = count_of_loads.find_element(By.ID, 'EventsPerPage_ALL')
    # print(element)
    # element.clear()
    # element.send_keys("200")

    # select_element = Select(count_of_loads.find_element(By.CLASS_NAME, 't-select'))
    # select_element.select_by_visible_text("200")
    time.sleep(5)
    # select_element = Select(browser.find_element(By.ID, "per_page_count"))


    # table = browser.find_element(By.ID, "ajaxPanel1")
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


def one_disp_dashboard(login, password, url, browser):
    one_disp_login(login, password, URL_DASH, browser)

    webdriver.Chrome().get(URL_DASH)

    pu_del_table = browser.find_element(By.ID, "dispatched_loads_ppu")
    pu_del_table_html = pu_del_table.get_attribute('outerHTML')
    html_io = StringIO(pu_del_table_html)
    df = pd.read_html(html_io)
    print(pu_del_table_html)
    # print(df)


getting_all_table(login=login, password=password, url=URL, browser=browser)
# one_disp_dashboard(login, password, URL_DASH, browser)
#

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import settings
from io import StringIO
from selenium.webdriver.support.ui import Select


URL = 'https://www.1dispatch.com/Carrier/CarrierViewHistory?DataType=ReLoad'
login = settings.ONE_DISP['login']
password = settings.ONE_DISP['password']
URL_DASH = 'https://www.1dispatch.com/Carrier/CarrierDashboard'

browser = webdriver.Chrome()


def one_disp_login(login, password, url, browser):
    browser.get(url)
    if browser.find_element(By.CLASS_NAME, "formdisplay"):
        browser.find_element(By.ID, "UserName").send_keys(login)
        browser.find_element(By.ID, "Password").send_keys(password)
        browser.find_element(By.ID, "btnLogin").click()


def getting_all_table(login, password, url, browser):
    one_disp_login(login, password, URL, browser)

    browser.find_elements(By.ID, "CarrierViewHistory_Menu")[1].click()

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

    select_element = Select(browser.find_element(By.ID, "perpage"))
    select_element.select_by_visible_text("All")


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


def one_disp_dashboard(login, password, url, browser):
    one_disp_login(login, password, URL_DASH, browser)

    webdriver.Chrome().get(URL_DASH)

    pu_del_table = browser.find_element(By.ID, "dispatched_loads_ppu")
    pu_del_table_html = pu_del_table.get_attribute('outerHTML')
    html_io = StringIO(pu_del_table_html)
    df = pd.read_html(html_io)
    print(pu_del_table_html)
    # print(df)


getting_all_table(login, password, URL, browser)
# one_disp_dashboard(login, password, URL_DASH, browser)


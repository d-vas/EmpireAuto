import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import settings
from SD_getting_loads import filling_sheet, open_file
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time



URL = 'https://www.1dispatch.com/Carrier/CarrierViewHistory?DataType=ReLoad'
login = settings.ONE_DISP['login']
password = settings.ONE_DISP['password']

cookies = requests.get(URL).cookies.get_dict()

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome(options=chrome_options, executable_path=r"C:\chromedriver.exe") #home
# browser = webdriver.Chrome(options=chrome_options) #work

one_dispatch_list = []
one_dispatch_list_pu = []
one_dispatch_list_del = []


def get_address_from_link_selenium(load_link):
    # one_disp_login(login, password, load_link, browser=browser)
    browser.get(load_link)
    res = browser.find_element(By.CLASS_NAME, 'subgridhead')
    load_info = res.find_element(By.CLASS_NAME, 'loadcontent ')
    pu_loc = load_info.find_elements(By.TAG_NAME, 'td')[3].text
    del_loc = load_info.find_elements(By.TAG_NAME, 'td')[4].text
    return pu_loc, del_loc


def onedisp_elem_to_dict(elem): #making one load-elem to dict
    txt = elem.text
    lst = txt.split('\n')

    dct = dict()

    dct['load_id'] = lst[2].split()[2]
    dct['total_price'] = lst[4].split()[-1]
    dct['vins'] = lst[3]
    dct['car_name'] = lst[5]
           # 'pu_loc': lst[7],
           # 'del_loc': lst[10],
    dct['pu_del_status'] = lst[-4]
    dct['expect_date'] = f"{lst[-3].split()[-1]} - {lst[-4]}"
    dct['customer/broker'] = lst[0].split('Shipper: ')[-1]
    dct['vehicles_count'] = int(lst[2].split()[4])
    dct['load_info'] = f"{lst[2].split()[2]}\n\n{lst[3]} - {lst[5]}\n\nASSIGNED to {lst[6].split()[2] + ' ' + lst[6].split()[3]}\n\n{lst[7]} - > {lst[10]}"

    if '/' in lst[6].split()[2]:
        dct['driver'] = "no driver assigned"
    else:
        dct['driver'] = lst[6].split()[2] + ' ' + lst[6].split()[3]
    dct['lnk'] = elem.find_element(By.TAG_NAME, 'a').get_attribute("href")
    # print(lnk)
    # dct['pu_loc'] = get_address_from_link_selenium(lnk)[0]

    return dct


def one_disp_sort_pu_del(lst, lst_pu, lst_del):
    for l in lst:
        if l['pu_del_status'] == 'Pending Pickup':
            lst_pu.append(l)
        elif l['pu_del_status'] == 'Pending Delivery':
            lst_del.append(l)
    lst.remove(l)


def one_disp_login(login, password, url, browser):
    browser.get(url)
    if browser.find_element(By.CLASS_NAME, "formdisplay"):
        browser.find_element(By.ID, "UserName").send_keys(login)
        browser.find_element(By.ID, "Password").send_keys(password)
        browser.find_element(By.ID, "btnLogin").click()


def getting_all_table(login, password, browser, load_list):
    one_disp_login(login, password, URL, browser)

    browser.find_elements(By.ID, 'CarrierViewHistory_Menu')[-1].click() #clicking btn "My Loads'
    browser.find_element(By.ID, "per_page_count").click() #choosing "Loads per page"
    list_of_options = browser.find_elements(By.CLASS_NAME, "t-animation-container")
    list_of_options[-1].find_elements(By.CLASS_NAME, 't-item')[-1].click() #clicking on last option in list of amounts

    pu_del_lst = browser.find_element(By.XPATH, '/html/body/div[3]') #clicking on btn "Select status"
    browser.execute_script("arguments[0].style.display = 'block';", pu_del_lst) #making list of status visible
    select_list = browser.find_element(By.XPATH, '/html/body/div[3]/ul')
    select_list.find_element(By.ID, 'ui-multiselect-filterStatus-option-1').click() #select "Pending Pick up"
    select_list.find_element(By.ID, 'ui-multiselect-filterStatus-option-2').click() #select "Pending Delivery"
    pu_del_lst.find_element(By.ID, 'btnFilterStatus').click() #click "Apply"

    div1 = browser.find_element(By.ID, 'GridCarrierLoadViewHistory') #whole table of loads
    table = div1.find_elements(By.CLASS_NAME, 'grsdTbl') #list of loads-elements
    return table



    # get_list_of_loads(table, one_dispatch_list)


if __name__ == '__main__':

    listofloadselements = getting_all_table(login=login, password=password, browser=browser, load_list=one_dispatch_list)

    for j in listofloadselements:
        dct_load = onedisp_elem_to_dict(j)
        one_dispatch_list.append(dct_load)
        # print(dct_load)

    for k in one_dispatch_list:
        k['pu_loc'] = get_address_from_link_selenium(k['lnk'])[0]
        k['del_loc'] = get_address_from_link_selenium(k['lnk'])[1]
        # print(pu)
        # print(deliv)

    one_disp_sort_pu_del(lst=one_dispatch_list, lst_pu=one_dispatch_list_pu, lst_del=one_dispatch_list_del)

    # for i in one_dispatch_list_pu:
    #     print(i)
    print(len(one_dispatch_list_pu))
    # for i in one_dispatch_list_del:
    #     print(i)
    print(len(one_dispatch_list_del))


    filling_sheet(sheet_name='1disp_pu', f=open_file(), load_list=one_dispatch_list_pu)

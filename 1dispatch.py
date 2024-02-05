from selenium import webdriver
from selenium.webdriver.common.by import By
import settings
from SD_getting_loads import filling_sheet, open_file


URL = 'https://www.1dispatch.com/Carrier/CarrierViewHistory?DataType=ReLoad'
login = settings.ONE_DISP['login']
password = settings.ONE_DISP['password']

browser = webdriver.Chrome(executable_path=r"C:\chromedriver.exe")

one_dispatch_list = []
one_dispatch_list_pu = []
one_dispatch_list_del = []


def one_disp_sort_pu_del(lst, lst_pu, lst_del):
    for i in lst:
        if i['pu_del_status'] == 'Pending Pickup':
            lst_pu.append(lst.pop(i))
        else:
            lst_del.append(lst.pop(i))

def get_list_of_loads(list_of_elem, load_list):
    for i in list_of_elem:
        dct = one_disp_text_to_dict(i.text)
        load_list.append(dct)

def one_disp_text_to_dict(text):
    lst = text.split('\n')
    dct = {'load_id': lst[2].split()[2],
           'total_price': lst[4].split()[-1],
           'vins': lst[3],
           'car_name': lst[5],
           'driver': lst[6].split()[2] + ' ' + lst[6].split()[3],
           'pu_loc': lst[7],
           'del_loc': lst[10],
           'pu_del_status': lst[-4],
           'expect_date': f"{lst[-3].split()[-1]} - {lst[-4]}",
           'customer/broker': lst[0].split('Shipper: ')[-1],
           'vehicles_count': lst[2].split()[4]}
    return dct


def one_disp_login(login, password, url, browser):
    browser.get(url)
    if browser.find_element(By.CLASS_NAME, "formdisplay"):
        browser.find_element(By.ID, "UserName").send_keys(login)
        browser.find_element(By.ID, "Password").send_keys(password)
        browser.find_element(By.ID, "btnLogin").click()


def getting_all_table(login, password, browser, load_list):
    one_disp_login(login, password, URL, browser)

    browser.find_elements(By.ID, 'CarrierViewHistory_Menu')[-1].click()
    browser.find_element(By.ID, "per_page_count").click()
    list_of_options = browser.find_elements(By.CLASS_NAME, "t-animation-container")
    list_of_options[-1].find_elements(By.CLASS_NAME, 't-item')[-1].click()

    pu_del_lst = browser.find_element(By.XPATH, '/html/body/div[3]')
    browser.execute_script("arguments[0].style.display = 'block';", pu_del_lst)
    select_list = browser.find_element(By.XPATH, '/html/body/div[3]/ul')
    select_list.find_element(By.ID, 'ui-multiselect-filterStatus-option-1').click()
    select_list.find_element(By.ID, 'ui-multiselect-filterStatus-option-2').click()
    pu_del_lst.find_element(By.ID, 'btnFilterStatus').click()

    div1 = browser.find_element(By.ID, 'GridCarrierLoadViewHistory')
    table = div1.find_elements(By.CLASS_NAME, 'grsdTbl')
    # print(table[0].text)
    get_list_of_loads(table, load_list)

    for i in one_disp_text_to_dict(table[0].text):
        print(i, ' - ', one_disp_text_to_dict(table[0].text)[i])


getting_all_table(login=login, password=password, browser=browser, load_list=one_dispatch_list)

# for i in one_dispatch_list:
#     print(i)

filling_sheet(sheet_name='1disp_pu', f=open_file(), load_list=one_dispatch_list)
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import settings
from SD_getting_loads import filling_sheet, open_file
from selenium.webdriver.chrome.options import Options



URL = 'https://www.1dispatch.com/Carrier/CarrierViewHistory?DataType=ReLoad'
login = settings.ONE_DISP['login']
password = settings.ONE_DISP['password']


cookies = requests.get(URL).cookies.get_dict()


# chrome_options = Options()
# chrome_options.add_argument("--headless")
browser = webdriver.Chrome(executable_path=r"C:\chromedriver.exe") #home
# browser = webdriver.Chrome(options=chrome_options) #work

one_dispatch_list = []
one_dispatch_list_pu = []
one_dispatch_list_del = []


def get_address_from_link_selenium(load_link, browser):
    browser.get(load_link)
    pu_address = browser.find_element(By.XPATH, r'/html/body/div[1]/div[3]/section/div[5]/form/table/tbody/tr[2]/td/div[1]/table/tbody/tr[5]/td[4]')
    # pu_address = browser.find_elements(By.CLASS_NAME, 'loadcontent')
    # table = browser.find_elements(By.TAG_NAME, 'table')
    # t1 = table[1].find_element(By.CLASS_NAME, 'LoadDetail')
    # pu_address = table.find_element(By.CLASS_NAME, 'subgridhead')
    # pu_address = browser.find_element(By.CSS_SELECTOR, '#frmLoadDetails > table > tbody > tr:nth-child(2) > td > div.LoadDetail > table > tbody > tr.loadcontent > td:nth-child(4)')
    print(pu_address)
    print(len(table))
    print(table[4].text)


def get_address_from_link(load_link, cookies):
    load_info = requests.get(load_link, cookies)
    # data = load_info.
    # print(data)
    # "//*[@id="frmLoadDetails"]/table/tbody/tr[2]/td/div[1]/table/tbody/tr[5]/td[4]"



def one_disp_text_to_dict(text): #making one load-elem to dict
    lst = text.split('\n')
    dct = {'load_id': lst[2].split()[2],
           'total_price': lst[4].split()[-1],
           'vins': lst[3],
           'car_name': lst[5],
           'pu_loc': lst[7],
           'del_loc': lst[10],
           'pu_del_status': lst[-4],
           'expect_date': f"{lst[-3].split()[-1]} - {lst[-4]}",
           'customer/broker': lst[0].split('Shipper: ')[-1],
           'vehicles_count': int(lst[2].split()[4]),
           'load_info': f"{lst[2].split()[2]}\n\n{lst[3]} - {lst[5]}\n\nASSIGNED to {(lst[6].split()[2] + ' ' + lst[6].split()[3]).upper()}\n\n{lst[7]} - > {lst[10]}",
           'link': f""}
    if '/' in lst[6].split()[2]:
        dct['driver'] = 'no driver assigned'
    else:
        dct['driver'] = lst[6].split()[2] + ' ' + lst[6].split()[3]
    return dct


def one_disp_sort_pu_del(lst, lst_pu, lst_del):
    for l in lst:
        if l['pu_del_status'] == 'Pending Pickup':
            lst_pu.append(l)
        elif l['pu_del_status'] == 'Pending Delivery':
            lst_del.append(l)
    lst.remove(l)


def get_list_of_loads(list_of_elem, load_list):
    for i in list_of_elem:
        lnk = i.find_element(By.TAG_NAME, 'a').get_attribute("href")
        dct = one_disp_text_to_dict(i.text)
        dct['link'] = lnk
        load_list.append(dct)


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
    table = div1.find_elements(By.CLASS_NAME, 'grsdTbl') #list of loads-elems
    # print(type(table))
    '''for i in table:
        lnk = i.find_element(By.TAG_NAME, 'a')
        print(lnk)'''
    get_list_of_loads(table, load_list=one_dispatch_list)

    # for i in one_dispatch_list:
    #     print(i)
    # print(len(one_dispatch_list))



if __name__ == '__main__':

    '''get_address_from_link_selenium(
        'https://1dispatch.com/Carrier/GetLoadDetailForCarrier?marketId=26666462&&Page=CarrierHistoryPartilaView',
        browser=browser)'''

    getting_all_table(login=login, password=password, browser=browser, load_list=one_dispatch_list)
    # print(f"total - {len(one_dispatch_list)}")
    one_disp_sort_pu_del(lst=one_dispatch_list, lst_pu=one_dispatch_list_pu, lst_del=one_dispatch_list_del)

    # for i in one_dispatch_list_pu:
    #     print(i)
    print(len(one_dispatch_list_pu))

    # for i in one_dispatch_list_del:
    #     print(i)
    print(len(one_dispatch_list_del))

    filling_sheet(sheet_name='1disp_pu', f=open_file(), load_list=one_dispatch_list_pu)




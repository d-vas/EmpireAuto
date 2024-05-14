import requests
import schedule
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from settings import sentral_dispatch_log_pass
from SD_getting_loads import filling_sheet, open_file
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.chrome.service import Service


start_time = time.time()

url = 'https://app.centraldispatch.com/dispatch'
url_login = 'https://id.centraldispatch.com/Account/Login'
url_main = 'centraldispatch.com'

# cookies = requests.get(url).cookies.get_dict()
headers = requests.get(url).headers
print(headers)


service = Service(r'C:\chromedriver.exe')
browser = webdriver.Chrome(service=service)

# browser = webdriver.Chrome(executable_path=r"C:\chromedriver.exe") #home
# browser.get(url_login)
# cookies = browser.get_cookies()
# browser.add_cookie(cookies)

login = sentral_dispatch_log_pass['login']
password = sentral_dispatch_log_pass['password']


def cd_login(login, password, url, browser):
    browser.get(url)
    browser.find_element(By.ID, "Username").send_keys(login)
    browser.find_element(By.ID, "password").send_keys(password)
    browser.find_element(By.ID, "loginButton").click()


def get_load_info_from_elem(elem):
    text = elem.text.replace('RECENTLY ADDED\n', '').replace('The pick-up date and delivery date are past due.\n', '')
    dct = {}
    dct['load_id'] = text.split('\n')[0]
    dct['status'] = text.split('\n')[1]
    dct['price'] = text.split('\n')[11]
    dct['car'] = text.split('\n')[13]
    dct['driver'] = text.split('\n')[15]
    dct['pu_loc'] = text.split('\n')[18]
    dct['del_loc'] = text.split('\n')[24]
    dct['load_info'] = text.split("\n")[0], '\n\n', (text.split('\n')[1]).upper, '\n\n', text.split('\n')[13], '\n\n', \
        text.split('\n')[15], '\n\n', text.split('\n')[18], ' --> ', text.split('\n')[24]

    return dct


def cd_sort_pu_del(lst, lst_pu, lst_del):
    for l in lst:
        if l['status'] == 'Dispatched':
            lst_pu.append(l)
        elif l['status'] == 'Picked-Up':
            lst_del.append(l)
    lst.remove(l)


def main():
    cd_load_list = []
    cd_load_list_pu = []
    cd_load_list_del = []

    cd_login(login=login, password=password, url=url_login, browser=browser)
    browser.get(url)

    whole_table = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'cd-dispatch-jss230')))
    list_of_loads_elem = whole_table.find_elements(By.XPATH, 'div')

    for i in list_of_loads_elem:
        cd_load_list.append(get_load_info_from_elem(i))

    cd_sort_pu_del(lst=cd_load_list, lst_pu=cd_load_list_pu, lst_del=cd_load_list_del)
    print(len(cd_load_list_pu))
    print(len(cd_load_list_del))
    # filling_sheet(sheet_name='cd_pu', f=open_file(), load_list=cd_load_list_pu)
    #
    # end_time = time.time()
    # duration = end_time - start_time
    # print("Час виконання: {:.2f} секунд".format(duration))


if __name__ == '__main__':
    main()
    schedule.every(10).minutes.do(main)
    while True:
        schedule.run_pending()


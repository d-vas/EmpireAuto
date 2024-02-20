import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from settings import carsarrive_log_pass
from SD_getting_loads import filling_sheet, open_file
from selenium.webdriver.chrome.options import Options


LOGIN_URL = 'https://login.carsarrive.com/?q=sso/idplogin'
BASE_URL = 'https://www.carsarrive.com/tab/TransportManager/Default.asp'


login = carsarrive_log_pass['login']
password = carsarrive_log_pass['password']


chrome_options = Options()
chrome_options.add_argument("--headless")
# browser = webdriver.Chrome(executable_path=r"C:\chromedriver.exe") #home
browser = webdriver.Chrome(options=chrome_options) #work


def ca_login(login, password, url, browser):
    browser.get(url)
    if browser.find_element(By.CLASS_NAME, "formdisplay"):
        browser.find_element(By.ID, "UserName").send_keys(login)
        browser.find_element(By.ID, "Password").send_keys(password)
        browser.find_element(By.ID, "btnLogin").click()


# session = requests.Session()
# response = session.post(LOGIN_URL, data=carsarrive_log_pass)

'''if response.status_code == 200:
    print("Login successful!")

    response_2 = session.get(BASE_URL)
    print(response_2.text)
    print(response_2.)
else:
    print(f"Login failed with status code: {response.status_code}")'''



'''selenium needed'''


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from settings import ZIPS


def determine_region(pu_zip, del_zip, zips):
    for i in zips:
        if pu_zip in zips[i]:
            pu_range = zips[i]
    for i in zips:
        if del_zip in zips[i]:
            del_range = zips[i]
    # print(pu_range)
    # print(del_range)
    return pu_range, del_range


def acv_login_getting_table(login, password):
    url = 'https://transport-v1.acvauctions.com/jobs/available.php'

    browser = webdriver.Chrome()

    browser.get(url)
    if browser.find_element(By.XPATH, "//*[contains(text(), 'Welcome')]"):
        browser.find_element(By.ID, "username").send_keys(login)
        browser.find_element(By.ID, "password").send_keys(password)
        browser.find_element(By.XPATH, "/html/body/div/main/section/div/div/div/form/div[3]").click()

    # show_all
    select_element = Select(browser.find_element(By.ID, "perpage"))
    select_element.select_by_visible_text("All")

    # get_table
    tables = browser.find_elements(By.CSS_SELECTOR, "table") #res list of selenium elements
    table = tables[2] #res - sel elem
    table_html = table.get_attribute('outerHTML') #res - html-str
    # print(table_html)


def acv_getting_list(table_html, pu_zip_range, del_zip_range, pu_zip, del_zip):
    df = pd.read_html(table_html)[0]
    df = df.fillna('NONE')
    df = df.iloc[5:-1]
    df.columns = df.iloc[0]

    df = df.iloc[1:]
    df = df.drop(columns=['NONE', 'DT', 'Date', 'Inop?', 'Address', 'Distance'])
    df.columns = ['Order ID', 'Vehicle', 'PU_City', 'PU_State', 'PU_Zip', 'DEL_City', 'DEL_State', 'DEL_Zip', 'Payout']

    albany_ZIP_list = ['120', '121', '122', '123', '124', '125']
    filtered_df = df[(df['PU_State'] == 'NY') & (df['DEL_State'] == 'NY')]

    # make zip int
    filtered_df['PU_Zip'] = filtered_df['PU_Zip'].astype(int)
    filtered_df['DEL_Zip'] = filtered_df['DEL_Zip'].astype(int)

    # filter table by zip
    filtered_df = filtered_df[filtered_df['PU_Zip'] in pu_zip_range]
    filtered_df = filtered_df[filtered_df['DEL_Zip'] in del_zip_range]

    # print(filtered_df)


determine_region(13206, 14001, ZIPS)
# table_html = acv_login_getting_table(settings.ACV['login'], settings.ACV['pass'])
# acv_getting_list(table_html, pu_zip, del_zip)


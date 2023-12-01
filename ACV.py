import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from settings import ZIPS
import settings


pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', 5)
pd.set_option('display.width', 1000)
# pd.set_option('display.multi_sparse', False)


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
    return table_html


def acv_getting_list(table_html, pu_zip, del_zip, zips):
    df = pd.read_html(table_html)[0]
    df = df.fillna('NONE')
    df = df.iloc[5:-1]
    df.columns = df.iloc[0]
    df = df.iloc[1:]
    df = df.drop(columns=['NONE', 'DT', 'Date', 'Inop?', 'Address', 'Distance'])
    df.columns = ['Order ID', 'Vehicle', 'PU_City', 'PU_State', 'PU_Zip', 'DEL_City', 'DEL_State', 'DEL_Zip', 'Payout']
    # df.set_index('Order ID', inplace=True)
    df['PU_Zip'] = df['PU_Zip'].astype(int)
    df['DEL_Zip'] = df['DEL_Zip'].astype(int)

    pu_range = []
    del_range = []

    for i in zips:
        if pu_zip in zips[i]:
            pu_range = zips[i]
            # print(i, ' - ', pu_range)
    for i in zips:
        if del_zip in zips[i]:
            del_range = zips[i]
            # print(i, ' - ', del_range)

    # print(df)
    # print()
    # print(pu_range, del_range, sep='\n')

    # print(min(pu_range), max(pu_range))
    # print(type(min(pu_range)), type(max(pu_range)))

    # filtered_df = df[min(pu_range) > df['PU_Zip'] < max(pu_range)]
    filtered_df = df[df['PU_Zip'] > min(pu_range)]
    filtered_df = filtered_df[df['PU_Zip'] < max(pu_range)]
    filtered_df = filtered_df[df['DEL_Zip'] > min(del_range)]
    filtered_df = filtered_df[df['DEL_Zip'] < max(del_range)]

    # print(filtered_df)
    # print()
    # print(filtered_df.to_dict())

    # filtered_df = filtered_df.iloc[0:]
    # print(filtered_df)

    # df = df[df['DEL_Zip'] in del_range]
    # filtered_df = filtered_df[filtered_df['DEL_Zip'] in del_zip_range]

    # print(df)

    # df_dict = filtered_df['Order ID'].to_dict()
    #
    # for i in df_dict:
    #     print(i, ' - ', df_dict[i])

    marged_df = filtered_df

    marged_df['pu_address'] = filtered_df['PU_City'] + ', ' + filtered_df['PU_State'] + ' ' + filtered_df['PU_Zip'].astype(str)
    marged_df['del_address'] = filtered_df['DEL_City'] + ', ' + filtered_df['DEL_State'] + ' ' + filtered_df['DEL_Zip'].astype(str)
    columns_to_drop = ['PU_City', 'PU_State', 'PU_Zip', 'DEL_City', 'DEL_State', 'DEL_Zip']
    marged_df.drop(columns=columns_to_drop, inplace=True)
    marged_df['Price'] = marged_df.pop('Payout')
    # marged_df.drop(columns=['PU_City', 'PU_State', 'PU_Zip', 'DEL_City', 'DEL_State', 'DEL_Zip'])

    # print(marged_df)
    # print('count = ', len(marged_df))
    #
    # # df_dict = marged_df.set_index('Order ID').to_dict(orient='index')
    # df_dict = marged_df.set_index('Order ID').to_dict()
    # print(df_dict)

    result_dict = {}

    for index, row in marged_df.iterrows():
        key = row['Order ID']
        values = row.drop('Order ID').tolist()
        result_dict[key] = values

    print(result_dict)
    print()

    for i in result_dict:
        print(i, ' - ', result_dict[i])
    print('count =', len(result_dict))

table_html = acv_login_getting_table(settings.ACV['login'], settings.ACV['pass'])
acv_getting_list(table_html, 13202, 12205, ZIPS)


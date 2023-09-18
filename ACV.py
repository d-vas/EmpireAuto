import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import settings

username = 'empire120@gmail.com'
password = 'TRANz@1212'

# login_url = 'https://odd-fire-7909.auth0.com/u/login?state=hKFo2SB2ekplRUVmc1NlT3NSVVhlYjFKVnl4YzdSYklyUTNHZaFur3VuaXZlcnNhbC1sb2dpbqN0aWTZIGhDZWlLcWxIR3R6Rm9nblV5WkdiajVLeGVBSl9zUTR6o2NpZNkgTWJjY1pTQ1djY01WSXZtVDJYZG9PQlVhSDFkUml5Rko'
data_url = 'https://transport-v1.acvauctions.com/jobs/available.php'

# browser = webdriver.Chrome('.chromedriver.exe')
browser = webdriver.Chrome()

# browser = webdriver.Chrome(executable_path='C:/Users/EMPIR/PycharmProjects/EmpireAuto/chromedriver.exe')
browser.get(data_url)
if browser.find_element(By.CLASS_NAME, "c7e7bd22b"):
    browser.find_element(By.ID, "username").send_keys("empire120@gmail.com")
    browser.find_element(By.ID, "password").send_keys("TRANz@1212")
    browser.find_element(By.CLASS_NAME, "cf0cbcb69").click()

# show_all
select_element = Select(browser.find_element(By.ID, "perpage"))
select_element.select_by_visible_text("All")

# get_table
tables = browser.find_elements(By.CSS_SELECTOR, "table") #res list of selenium elements
table = tables[2] #res - sel elem
table_html = table.get_attribute('outerHTML') #res - html-str

df = pd.read_html(table_html)[0]
df = df.fillna('NONE')
df = df.iloc[5:-1]
df.columns = df.iloc[0]

df = df.iloc[1:]
df = df.drop(columns=['NONE', 'DT', 'Date', 'Inop?', 'Address', 'Distance'])
df.columns = ['Order ID', 'Vehicle', 'PU_City', 'PU_State', 'PU_Zip', 'DEL_City', 'DEL_State', 'DEL_Zip', 'Payout']

albany_ZIP_list = ['120', '121', '122', '123', '124', '125']
filtered_df = df[(df['PU_State'] == 'NY') & (df['DEL_State'] == 'NY')]

# print(filtered_df.dtypes)
filtered_df['PU_Zip'] = filtered_df['PU_Zip'].astype(int)
filtered_df['DEL_Zip'] = filtered_df['DEL_Zip'].astype(int)
# filtered_df.loc[:, 'PU_Zip'] = filtered_df['PU_Zip'].astype(int)
# filtered_df.loc[:, 'DEL_Zip'] = filtered_df['DEL_Zip'].astype(int)
# print(filtered_df.dtypes)

filtered_df = filtered_df[filtered_df['DEL_Zip'] >= 12000]
filtered_df = filtered_df[12599 >= filtered_df['DEL_Zip']]
# filtered_df = filtered_df[filtered_df[12599 <= filtered_df['PU_Zip'] >= 12000]] # not works
# filtered_df = filtered_df[str(filtered_df['DEL_Zip'][0:3]) in albany_ZIP_list] # not works


print(filtered_df)

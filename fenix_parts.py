import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd


scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('empireauto1-bf404e4d35b2.json', scope)
client = gspread.authorize(credentials)

spreadsheet = client.open("Fenix Parts Corporate")

worksheet = client.open("Active")

data = worksheet.get_all_values()

df = pd.DataFrame(data[1:], columns=data[0])

print(df)
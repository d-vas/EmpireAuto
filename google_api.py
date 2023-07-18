import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from bot_v20 import cars


def append_new_row_to_empire_ss(row):
    scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('empireauto1-bf404e4d35b2.json', scope)
    client = gspread.authorize(credentials)

    # sheet.share('dzyadekvl@gmail.com', perm_type='user', role='writer')
    # sheet.share('empire120@gmail.com', perm_type='user', role='writer')

    sheet = client.open("EmpireAuto/firstsheet").worksheet('Sheet1')
    sheet.append_row(row)


append_new_row_to_empire_ss(cars[0])


# worksheets("Sheet1")
# df = pd.DataFrame(columns=['driver_name', 'driver_age'])


# new_row = pd.Series(['vas', '123', '0000'], index=['driver_1', 'load_id', 'internal_load_id'])
# last_row_index = len(sheet.get_all_values()) + 1
# sheet.insert_row(new_load_row, index=2)

# df = pd.DataFrame(columns=['name', 'age'])
#
# header = ['Колонка 1', 'Колонка 2', 'Колонка 3']
# values = df[header].values.tolist()
# sheet.insert_row(header, 1)
# sheet.insert_rows(values, 2)

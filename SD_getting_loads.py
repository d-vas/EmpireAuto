import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('empireauto1-bf404e4d35b2.json', scope)
client = gspread.authorize(credentials)
file_of_sheets = client.open("EmpireAuto/firstsheet")


base_url = 'https://carrier.superdispatch.com/internal/web/loads/new/?page='

cookies = requests.get(base_url).cookies.get_dict()
headers = {"authorization": "Token 907fb140aebd44d799399ee4d9d2a443",}

load_list = []
florida_load_list = []
dispatched_load_list = []


def filling_sheet(sheet_name, f, load_list):
    sheet = f.worksheet(sheet_name)
    sheet.clear()
    sheet.append_row(list(load_list[0].keys()))
    for i in load_list:
        new_row = []
        for j in i:
            new_row.append(i[j])
        sheet.append_row(new_row)


def cleanse_vehicle(dct):
    dct['car_name'] = str(dct['year']) + ' ' + dct['make'] + ' ' + dct['model']
    key_list_to_remove = ['guid', 'make', 'model', 'year', 'color', 'requires_enclosed_trailer', 'type', 'lot_number', 'is_inoperable', 'price',]
    for i in key_list_to_remove:
        del dct[i]


def get_new_loads_list(base_url, headers, cookies, counter, load_list):
    url = base_url + str(counter)
    r = requests.get(url, headers=headers, cookies=cookies)
    data_list = r.json()['data']
    load_list.extend(data_list)
    if len(data_list) == 10:
        counter += 1
        get_new_loads_list(base_url=base_url, headers=headers, cookies=cookies, counter=counter, load_list=load_list)


def get_dispatched_load_list(load_list, dispatched_list):
    for i in load_list:
        if i['is_dispatched_to_carrier']:
            dispatched_list.append(i)


def get_florida_load_list(load_list, florida_load_list):
    for i in load_list:
        if i['delivery']['venue']['state'].upper() == 'FL':
            florida_load_list.append(i)


def cleance_load_dct(dct):
    key_list = ['number', 'pickup', 'delivery', 'customer', 'payments', 'vehicles', ]
    key_list_remove = set(dct.keys()) - set(key_list)
    for i in key_list_remove:
        del dct[i]

    dct['pickup'] = dct['pickup']['venue']
    dct['pickup_loc'] = f"{dct['pickup']['address']},  {dct['pickup']['city']}, {dct['pickup']['state']} {dct['pickup']['zip']}"
    del dct['pickup']['business_type']
    del dct['pickup']['contacts']

    dct['delivery'] = dct['delivery']['venue']
    del dct['delivery']['business_type']
    del dct['delivery']['contacts']
    dct['delivery_loc'] = f"{dct['delivery']['city']}, {dct['delivery']['state']} {dct['delivery']['zip']}"

    dct['vins'] = ''

    for i in dct['vehicles']:
        cleanse_vehicle(i)
        dct['vins'] += f"\n{i['vin']}"

    dct['customer'] = dct['customer']['venue']['name']
    dct['total_price'] = dct['payments'][0]['price']
    del dct['payments']

    dct['vehicles_count'] = len(dct['vehicles'])

    del dct['pickup']
    del dct['delivery']
    del dct['vehicles']


get_new_loads_list(base_url=base_url, headers=headers, cookies=cookies, counter=1, load_list=load_list)
# print(load_list[0].keys())
print(load_list[0])

get_dispatched_load_list(load_list=load_list, dispatched_list=dispatched_load_list)

get_florida_load_list(load_list=load_list, florida_load_list=florida_load_list)

for i in dispatched_load_list:
    if i in load_list:
        load_list.remove(i)

for i in florida_load_list:
    if i in load_list:
        load_list.remove(i)

for i in dispatched_load_list:
    cleance_load_dct(i)

for i in load_list:
    cleance_load_dct(i)

for i in florida_load_list:
    cleance_load_dct(i)

filling_sheet(sheet_name='new_loads', f=file_of_sheets, load_list=load_list)
filling_sheet(sheet_name='dispatched', f=file_of_sheets, load_list=dispatched_load_list)
filling_sheet(sheet_name='florida', f=file_of_sheets, load_list=florida_load_list)


print(len(load_list))
print(len(dispatched_load_list))
print(len(florida_load_list))
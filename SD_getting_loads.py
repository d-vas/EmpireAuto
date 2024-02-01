import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import settings


scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('empireauto1-bf404e4d35b2.json', scope)
client = gspread.authorize(credentials)
file_of_sheets = client.open("EmpireAuto/firstsheet")


base_url = 'https://carrier.superdispatch.com/internal/web/loads/new/?page='
assign_url = 'https://carrier.superdispatch.com/internal/web/loads/assigned/?page='
picked_up_url = 'https://carrier.superdispatch.com/internal/web/loads/picked-up/?page='


cookies = requests.get(base_url).cookies.get_dict()
# cookies = requests.get('https://carrier.superdispatch.com/').cookies.values()
headers = requests.get(base_url).headers
headers = settings.SD_headers_work

load_list = []
florida_load_list = []
dispatched_load_list = []
assigned_load_list = []
picked_up_load_list = []
key_list = []


def get_load_list(base_url, headers, cookies, counter, load_list):
    lst = load_list
    url = base_url + str(counter)
    r = requests.get(url, headers=headers, cookies=cookies)
    print(r.text)
    data_list = r.json()['data']
    load_list.extend(data_list)
    if len(data_list) == 10:
        counter += 1
        get_assign_loads_list(base_url=assign_url, headers=headers, cookies=cookies, counter=counter, load_list=lst)


def get_assign_loads_list(base_url, headers, cookies, counter, load_list):
    url = base_url + str(counter)
    r = requests.get(url, headers=headers, cookies=cookies)
    data_list = r.json()['data']
    load_list.extend(data_list)
    if len(data_list) == 10:
        counter += 1
        get_assign_loads_list(base_url=assign_url, headers=headers, cookies=cookies, counter=counter, load_list=assigned_load_list)


def filling_sheet(sheet_name, f, load_list):
    if load_list:
        sheet = f.worksheet(sheet_name)
        # assert isinstance(sheet, object)
        sheet.clear()
        list_of_lists = []
        list_of_lists.append(list(load_list[0].keys()))
        for i in load_list:
            list_of_lists.append(list(i.values()))
        sheet.update('A1', list_of_lists)


def cleanse_vehicle(dct):
    dct['car_name'] = f"{dct['year']} {dct['make']} {dct['model']}"
    key_list_to_remove = ['guid', 'make', 'model', 'year', 'color', 'requires_enclosed_trailer', 'type', 'lot_number', 'is_inoperable', 'price',]
    for i in key_list_to_remove:
        del dct[i]


def get_new_loads_list(base_url, headers, cookies, counter, load_list):
    url = base_url + str(counter)
    r = requests.get(url, headers=headers, cookies=cookies)
    # print(r)
    # print(r.json())
    data_list = r.json()['data']
    # print(len(data_list))
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
    key_list = ['number', 'pickup', 'delivery', 'customer', 'payments', 'vehicles', ] #, 'driver', 'terminals', 'online_bol_url', 'guid'
    key_list_remove = set(dct.keys()) - set(key_list)
    for i in key_list_remove:
        del dct[i]

    dct['pickup'] = dct['pickup']['venue']
    dct['pickup_loc'] = f"{dct['pickup']['address']},  {dct['pickup']['city']}, {dct['pickup']['state']} {dct['pickup']['zip']}"
    dct['pickup_city_zip'] = f"{dct['pickup']['city']}, {dct['pickup']['state']} {dct['pickup']['zip']}"
    del dct['pickup']

    dct['delivery'] = dct['delivery']['venue']
    dct['delivery_loc'] = f"{dct['delivery']['address']},  {dct['delivery']['city']}, {dct['delivery']['state']} {dct['delivery']['zip']}"
    dct['delivery_city_zip'] = f"{dct['delivery']['city']}, {dct['delivery']['state']} {dct['delivery']['zip']}"
    del dct['delivery']

    dct['customer'] = dct['customer']['venue']['name']
    dct['total_price'] = dct['payments'][0]['price']
    del dct['payments']

    dct['vins'] = ''
    for i in dct['vehicles']:
        cleanse_vehicle(i)
        dct['vins'] += f"\n{i['vin']} - {i['car_name']}"
    dct['vehicles_count'] = len(dct['vehicles'])
    del dct['vehicles']

    dct['load_info_for_pu'] = f"{dct['number']}\n{dct['vins']}\n\nDEL->{dct['delivery_city_zip']}"
    dct['load_info_for_del'] = f"{dct['number']}\nPU from{dct['delivery_city_zip']} ->"

# getting new load list
get_new_loads_list(base_url=base_url, headers=headers, cookies=cookies, counter=1, load_list=load_list)

get_dispatched_load_list(load_list=load_list, dispatched_list=dispatched_load_list)

get_florida_load_list(load_list=load_list, florida_load_list=florida_load_list)

get_assign_loads_list(base_url=assign_url, headers=headers, cookies=cookies, counter=1, load_list=assigned_load_list)



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

for i in assigned_load_list:
    cleance_load_dct(i)

filling_sheet(sheet_name='new_loads', f=file_of_sheets, load_list=load_list)
filling_sheet(sheet_name='dispatched', f=file_of_sheets, load_list=dispatched_load_list)
filling_sheet(sheet_name='florida', f=file_of_sheets, load_list=florida_load_list)
filling_sheet(sheet_name='assigned', f=file_of_sheets, load_list=assigned_load_list)
filling_sheet(sheet_name='delivery', f=file_of_sheets, load_list=load_list + assigned_load_list + picked_up_load_list)


print(f'new loads - {len(load_list)}')
print(f'dispatched - {len(dispatched_load_list)}')
print(f'florida - {len(florida_load_list)}')
print(f'assigned - {len(assigned_load_list)}')
print('_'*10, '\n', 'total new -', len(florida_load_list) + len(dispatched_load_list) + len(load_list))

# for i in assigned_load_list[0]:
#     print(f'{i} - {assigned_load_list[0][i]}')
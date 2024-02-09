import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import settings

base_url = 'https://carrier.superdispatch.com/internal/web/loads/new/?page='
assign_url = 'https://carrier.superdispatch.com/internal/web/loads/assigned/?page='
picked_up_url = 'https://carrier.superdispatch.com/internal/web/loads/picked-up/?page='
in_terminal_url = 'https://carrier.superdispatch.com/internal/web/loads/in-terminal/?page='

cookies = requests.get(base_url).cookies.get_dict()
headers = settings.SD_headers_work

new_load_list = []
florida_load_list = []
dispatched_load_list = []
assigned_load_list = []
picked_up_load_list = []
in_terminal_load_list = []


def get_florida_load_list(load_list, florida_load_list):
    for i in load_list:
        if i['delivery']['venue']['state'].upper() == 'FL':
            florida_load_list.append(i)
            load_list.remove(i)


def get_dispatched_load_list(load_list, dispatched_list):
    for i in load_list:
        if i['is_dispatched_to_carrier']:
            dispatched_list.append(i)
            load_list.remove(i)


def cleance_load_dct(dct):
    keys_list = ['number', 'pickup', 'delivery', 'customer', 'payments', 'vehicles'] #,  'terminals', 'online_bol_url', 'guid', 'status', 'stage' , 'driver'
    key_list_remove = set(dct.keys()) - set(keys_list)
    for i in key_list_remove:
        del dct[i]

    # if dct['driver']:
    #     dct['driver_name'] = dct['driver']['name']
    # else:
    #     dct['driver_name'] = 'NONAME'
    # del dct['driver']

    dct['load_id'] = dct.pop('number')

    dct['pickup'] = dct['pickup']['venue']
    dct['pickup_loc'] = f"{dct['pickup']['address']},  {dct['pickup']['city']}, {dct['pickup']['state']} {dct['pickup']['zip']}"
    dct['pickup_csz'] = f"{dct['pickup']['city']}, {dct['pickup']['state']} {dct['pickup']['zip']}"
    del dct['pickup']

    dct['delivery'] = dct['delivery']['venue']
    dct['delivery_loc'] = f"{dct['delivery']['address']}, {dct['delivery']['city']}, {dct['delivery']['state']} {dct['delivery']['zip']}"
    dct['delivery_csz'] = f"{dct['delivery']['city']}, {dct['delivery']['state']} {dct['delivery']['zip']}"
    del dct['delivery']

    dct['customer/broker'] = dct['customer']['venue']['name']
    del dct['customer']
    dct['total_price'] = dct['payments'][0]['price']
    del dct['payments']

    dct['vins'] = ''
    dct['vins_cars'] = ''
    for i in dct['vehicles']:
        dct['vins'] += f"\n{i['vin']}"
        dct['vins_cars'] += f"\n{i['vin']} - {i['year']} {i['make']} {i['model']}"
    dct['vehicles_count'] = len(dct['vehicles'])
    del dct['vehicles']

    dct['load_info'] = f"{dct['load_id']}\n\n{dct['vins_cars']}\n\n{dct['pickup_csz']} - > {dct['delivery_csz']}"


def open_file():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('empireauto1-bf404e4d35b2.json', scope)
    client = gspread.authorize(credentials)
    return client.open("EmpireAuto/loads")


def get_load_list(url, headers, cookies, counter, load_list):
    r = requests.get(url + str(counter), headers=headers, cookies=cookies)
    if 'data' in r.json().keys(): # r.json()['data']
        # print(r.json()['data'])
        data_list = r.json()['data']
        load_list.extend(data_list)
        if len(data_list) == 10:
            counter += 1
            get_load_list(url, headers=headers, cookies=cookies, counter=counter, load_list=load_list)
        # print(data_list)

def filling_sheet(sheet_name, f, load_list):
    sheet = f.worksheet(sheet_name)
    sheet.clear()
    if load_list:
        list_of_lists = [list(load_list[0].keys())]
        for d in load_list:
            # print(d)
            list_of_lists.append(list(d.values()))

        # for k in list_of_lists:
        #     print(k)

        sheet.update('A1', list_of_lists)


if __name__ == '__main__':

    get_load_list(url=base_url, headers=headers, cookies=cookies, counter=1, load_list=new_load_list)
    # get_dispatched_load_list(load_list=new_load_list, dispatched_list=dispatched_load_list)
    # get_florida_load_list(load_list=new_load_list, florida_load_list=florida_load_list)
    # get_load_list(url=assign_url, headers=headers, cookies=cookies, counter=1, load_list=assigned_load_list)
    # get_load_list(url=in_terminal_url, headers=headers, cookies=cookies, counter=1, load_list=in_terminal_load_list)
    # get_load_list(url=picked_up_url, headers=headers, cookies=cookies, counter=1, load_list=picked_up_load_list)
    for i in new_load_list:
        cleance_load_dct(i)
    # for i in assigned_load_list:
    #     cleance_load_dct(i)
    # for i in dispatched_load_list:
    #     cleance_load_dct(i)
    # for i in florida_load_list:
    #     cleance_load_dct(i)
    # for i in in_terminal_load_list:
    #     cleance_load_dct(i)
    # for i in picked_up_load_list:
    #     cleance_load_dct(i)

    filling_sheet(sheet_name='new_loads', f=open_file(), load_list=new_load_list)
    # filling_sheet(sheet_name='dispatched', f=open_file(), load_list=dispatched_load_list)
    # filling_sheet(sheet_name='florida', f=open_file(), load_list=florida_load_list)
    # filling_sheet(sheet_name='assigned', f=open_file(), load_list=assigned_load_list)
    # filling_sheet(sheet_name='in_terminal', f=open_file(), load_list=in_terminal_load_list)
    # filling_sheet(sheet_name='picked_up_url', f=open_file(), load_list=picked_up_load_list)

    print(f'new loads - {len(new_load_list)}')
    print(f'dispatched - {len(dispatched_load_list)}')
    print(f'florida - {len(florida_load_list)}')
    print(f'assigned - {len(assigned_load_list)}')
    print('_'*10, '\n', 'total new -', len(florida_load_list) + len(dispatched_load_list) + len(new_load_list))
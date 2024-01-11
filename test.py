import requests


base_url = 'https://carrier.superdispatch.com/internal/web/loads/new/?page='

cookies = requests.get(base_url).cookies.get_dict()

headers = {"authorization": "Token 907fb140aebd44d799399ee4d9d2a443",}

url_new = 'https://carrier.superdispatch.com/internal/web/loads/new/?page='

load_list = []

key_list = ['guid', 'stage', 'number', 'status', 'pickup', 'delivery', 'customer', 'payments', 'driver', 'terminals',
            'vehicles',]

def get_new_loads_sd(base_url, headers, cookies, counter, load_list):
    url = base_url + str(counter)
    r = requests.get(url, headers=headers, cookies=cookies)
    js = r.json()
    # print(js)
    # print(js['data'])
    data_list = js['data']
    load_list.extend(data_list)
    # for i in data_list:
    #     print(i)
    #     print()
    # print(len(data_list))

    if len(data_list) == 10:
        counter += 1
        get_new_loads_sd(base_url=url_new, headers=headers, cookies=cookies, counter=counter, load_list=load_list)
    return load_list


get_new_loads_sd(base_url=url_new, headers=headers, cookies=cookies, counter=1, load_list=load_list)
# print(get_new_loads_sd(base_url=url_new, headers=headers, cookies=cookies, counter=1, load_list=load_list))


'''for i in load_list:
    print(i)
print(len(load_list))
'''


'''print(load_list[0])
for j in load_list[0]:
    print(j, ' - ', load_list[0][j])
'''


my_dict = {key: load_list[1][key] for key in load_list[1] if key in key_list}

my_dict['pickup'] = my_dict['pickup']['venue']
my_dict['delivery'] = my_dict['delivery']['venue']
my_dict['payments'] = my_dict['payments'][0]
# my_dict['vehicles'] = my_dict['vehicles'][0]


# print(len(my_dict['vehicles']))


def cleanse_vehicle(dict):
    dict['car_name'] = str(dict['year']) + ' ' + dict['make'] + ' ' + dict['model'] + ' ' + dict['type']
    key_list_to_remove = ['guid', 'make', 'model', 'year', 'color', 'requires_enclosed_trailer',]
    for i in key_list_to_remove:
        del dict[i]


for i in my_dict['vehicles']:
    cleanse_vehicle(i)


for i in my_dict:
    print(i, ' - ', my_dict[i])
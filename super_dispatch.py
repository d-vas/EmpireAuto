


def get_drivers(text, load, activity, loc_text):

    ''' current_driver '''
    if 'Assigned' in loc_text:
        load['current_driver'] = ' '.join(re.findall(r"\bAssigned to \w+\s+\w+\b", text)[0].split()[-2:])
    else:
        load['current_driver'] = 'driver not assigned'

    if load['terminal']:
            driver_2_pattern = r"\w+ \w+ marked the order as delivered to destination"
            load['driver_2'] = ' '.join(re.findall(driver_2_pattern, activity)[0].split()[:2])

            driver_1_pattern = r"\w+ \w+ marked the order as delivered to terminal"
            load['driver_1'] = ' '.join(re.findall(driver_1_pattern, activity)[0].split()[:2])


def get_terminal(activity):
    if 'terminal' in activity:
        load['terminal'] = activity.split('terminal')[1].split()[0]
    else:
        load['terminal'] = ''


def get_dates(text):
    pu_pattern = r"Picked Up on\n\w{3} \d{1,}, \d{2,4}"
    del_pattern = r"Delivered on\n\w{3} \d{1,}, \d{2,4}"
    if 'Picked Up on' in text:
        load['pu_date'] = re.findall(pu_pattern, text)[0].split('\n')[1]
    if 'Delivered on' in text:
        load['del_date'] = re.findall(del_pattern, text)[0].split('\n')[1]


def get_cars(text):
    cars_txt = text.split('Price')[1].strip().split('Payment')[0]
    cars_txt = cars_txt.split('Inspection Details')[0].strip()
    cars_txt = cars_txt.split('Driver Instructions')[0].strip()
    vin_list = re.findall(r'\n[A-HJ-NPR-Z\d]{0,11}[A-HJ-NPR-Z\d]{2}\d{4}\s\n', cars_txt)
    vin_list = list(map(lambda x: x.strip(), vin_list))

    for i in range(1, len(vin_list)+1):
        key = f'car {i}'
        cars[key] = []
        cars[key].append(vin_list[i-1])   # adding vin at the beginning of the list
        temp_list = cars_txt.split(vin_list[i-1])[0].split('\n')
        temp_list = [elem for elem in temp_list if elem.strip()]

        cars[key].append(temp_list[-2])
        cars[key].append(temp_list[-1])

        vins = '\n'.join(vin_list)

        load['vin'] = vin_list
    return vin_list


def parse_super_disp_1load(update, text, load):
    loc_text = text.split('Internal Load ID:')[1].strip().split('Vehicle Details')[0].split('\n\n')[1]
    print(repr(loc_text))
    activity = text.split('Activity')[1]

    load.clear()
    cars.clear()

    load['load_id'] = text.split('Help')[1].strip().split('\n')[0]
    load['internal_load_id'] = text.split('Internal Load ID:')[1].strip().split('\n')[0].strip()
    load['load_status'] = text.split('Reports')[1].split('Internal Load ID:')[0].strip().split('\n')[-1]
    load['rate'] = text.split('Payment', maxsplit=1)[1].split('Method')[0].split('\n')[-2].strip()

    if 'Customer Information' in text:
        load['customer'] = text.split('Customer Information')[1].strip().split('\n')[0]
    else:
        load['customer'] = 'NO CUSTOMER'

    load['date_create'] = text.split('was')[-1].split('\n')[1]




    # add_row(list(load.keys()), sheet=sheet)
    get_terminal(activity)
    get_cars(text)
    get_drivers(loc_text, load, activity, loc_text)
    get_locations(loc_text)
    get_dates(loc_text)

    return f"{msg_from_dict(load)}\n{msg_from_dict(cars)}"


def get_locations(loc_text):
    address_pattern = r"\d+\s+\w+\s*\w*\s*\w*\s*\w*.*\b,\s*\w*\w*\s+\w+,\s+[A-Z]{2}\s+\d{5}"
    load['pu_address'], load['del_address'] = re.findall(address_pattern, loc_text)


load = {'load_id': None,
        'internal_load_id': None,
        'customer': None,
        'vin': None,
        'pu_date': None,
        'pu_name': None,
        'pu_address': None,
        'pu_city': None,
        'pu_zip': None,
        'del_date': None,
        'del_name': None,
        'del_address': None,
        'vehicle_count': None,
        'rate': None,
        'car': None,
        'driver_1': None,
        'driver_2': None,
        'driver_1_pay': None,
        'driver_2_pay': None,
        'terminal': None,
        'date_create': None,
        'terminal_date': None,
        'milage_1': None,
        'milage_2': None,
        'load_status': None,
        'current_terminal': None
        }

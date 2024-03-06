'''list_ = []
for i in cars_txt.split('\n'):
    if i not in ['', ' ', '\n', '\t', '\r\n', '\r']:
        list_.append(i)
list_ = list_[:-2] #temporary work car list
cars_list = []
for i in range(len(list_)//4):
    cars_list.append(list_[i:i+4])
    i += -1

work_text = cars_txt[:]'''



'''if 'terminal' in text:
    load['current_terminal'] = text.split('Reports')[1].strip().split('\n')[2]'''



'''
if 'marked the order as delivered to' in activity:
    drivers = re.findall(r'[A-Z]+\s[A-Z]+\smarked the order as delivered to', activity)
    drivers = list(map(lambda x: x.strip('marked the order as delivered to'), drivers))
    print(drivers)
    load['driver1'] = drivers[-1]
    if len(drivers) > 1:
        load['driver2'] = drivers[0]
    else:
        load['driver2'] = ''
if load['driver1']:
    spliter = f"{load['driver1']} marked the order as picked up from origin"
    load['pu_date_time'] = activity.split(spliter)[1].split('\n\n')[0].strip()
if load['driver2']:
    spliter = f"{load['driver2']} marked the order as delivered to destination"
    load['del_date_time'] = activity.split(spliter)[1].split('\n\n')[0].strip()
'''



def print_dict(dict_):
    for i in dict_:
        print(i, ':', dict_[i])



        # work_text = work_text.split(vin_list[i-1])[1]



# print(re.findall(r'\n\d+\s+\w+\s*\s+\w+,\s+[A-Z]{2}\s+\d{5}\n', text))



zip_code_pattern = r'^\d{5}(?:-\d{4})?$'



address_pattern = r"\n\d+\s+\w+\s*\w*\b,\w*\s+\w+,\s+[A-Z]{2}\s+\d{5}\n"




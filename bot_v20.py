from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import Update
import settings
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials


TOKEN = settings.TOKEN


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
        }

cars = {}


scope = ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('empireauto1-bf404e4d35b2.json', scope)
client = gspread.authorize(credentials)
sheet = client.open("EmpireAuto/firstsheet").worksheet('Sheet4')


def headers_list_new_row(sheet, load):
    new_row = []
    headers = sheet.row_values(1)
    print(headers)

    for column in headers:
        new_row.append(load[column])
    sheet.append_row(new_row)

def add_row(row_list, sheet):
    sheet.append_row(row_list)


def print_dict(dict_):
    for i in dict_:
        print(i, ':', dict_[i])


def msg_from_dict(dict_):
    msg = ''
    for i in dict_:
        msg = msg + f"{i} --- {dict_[i]}\n"
    return msg


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",)


def get_locations(text):
    loc_text = text.split('Internal Load ID:')[1].strip().split('Vehicle')[0]
    zip_code_pattern = r'^\d{5}(?:-\d{4})?$'
    address_pattern = r"\n\d+\s+\w+\s*\w*\b,\w*\s+\w+,\s+[A-Z]{2}\s+\d{5}\n"

    # print(repr(loc_text))

    if 'Assigned to' in loc_text:
        load['pu_name'] = loc_text.split('\n')[3]
        load['pu_address'] = loc_text.split('\n')[4]
    else:
        load['pu_name'] = loc_text.split('\n')[2]
        load['pu_address'] = loc_text.split('\n')[3]

    '''load['pu_address'] = text.split('Internal Load ID:')[1].strip().split('\n')[3]
    load['del_name'] = text.split('cheduled')[1].strip().split('cheduled')[0].strip().split('\n')[-3]
    load['del_address'] = text.split('cheduled')[1].strip().split('cheduled')[0].strip().split('\n')[-2]'''


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
        # work_text = work_text.split(vin_list[i-1])[1]


        vins = '\n'.join(vin_list)
        print(vins)

        load['vin'] = vin_list
    return vin_list


def parse_super_disp_1load(update, text, load=load):
    load.clear()


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

    load['load_id'] = text.split('Reports')[1].strip().split('\n')[0]
    load['internal_load_id'] = text.split('Internal Load ID:')[1].strip().split('\n')[0].strip()
    load['load_status'] = text.split('Reports')[1].split('Internal Load ID:')[0].strip().split('\n')[-1]

    '''if 'terminal' in text:
        load['current_terminal'] = text.split('Reports')[1].strip().split('\n')[2]'''

    # print(text.split('Payment', maxsplit=1)[1].split('Method')[0])
    load['rate'] = text.split('Payment', maxsplit=1)[1].split('Method')[0].split('\n')[-2].strip()
    if 'Customer Information' in text:
        load['customer'] = text.split('Customer Information')[1].strip().split('\n')[0]
    else:
        load['customer'] = 'NO CUSTOMER'



    load['date_create'] = text.split('was')[-1].split('\n')[1]
    if 'Assigned' in text:
        load['current_driver'] = text.split('Assigned to ')[1].split('\n')[0]
    else:
        load['current_driver'] = 'driver not assigned'

    activity = text.split('Activity')[1]

    if 'marked the order as delivered to' in activity:
        load['driver2'] = activity.split('marked the order as delivered to destination')[0].split('\n')[-1]

    drivers = re.findall(r'\b[A-Z]+\s[A-Z]+\b', activity)
    drivers_pu = re.findall(r'\b[A-Z]+\s[A-Z]+ marked the order as picked up from origin', activity)

    for i in range(len(drivers_pu)):
        drivers_pu[i] = ' '.join(drivers_pu[i].split()[0:2])
        # print(i)


    if 'terminal' in activity:
        load['terminal'] = activity.split('terminal')[1].split()[0]
    else:
        load['terminal'] = ''


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

    load['del_date_terminal'] = ''

    # add_row(list(load.keys()), sheet=sheet)



    print(re.findall(r'\n\d+\s+\w+\s*\s+\w+,\s+[A-Z]{2}\s+\d{5}\n', text))

    get_cars(text=text)

    get_locations(text)

    return f"{msg_from_dict(load)}\n{msg_from_dict(cars)}"


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    await update.message.reply_text(parse_super_disp_1load(update, text, load))


def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.run_polling()


# if __name__ == "__main__":
main()


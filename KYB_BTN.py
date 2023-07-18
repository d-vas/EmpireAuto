btn_trucks = 'trucks'
btn_drivers = 'drivers'
btn_yards = 'yards'
btn_office = 'office'
btn_loads = 'loads'

# main keyboard
def keyboard(btn_dict):
    pass

def btn_lst(btn_dict):
    return list(btn_dict.values())

print(btn_lst(buttons_names))

keyboard1 = [[InlineKeyboardButton(buttons_names['trucks'], callback_data='trucks')]]

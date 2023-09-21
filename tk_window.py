import tkinter as tk
import re


req_pu = {'city': '', 'state': '', 'zip': ''}
req_del = {'city': '', 'state': '', 'zip': ''}

'''
def get_split_locations(loc_text, req_dict):
    # print(loc_text.strip())
    address_pattern = r"\w*\s*\w*\s*\w+,\s+[A-Z]{2}(\s*\d{5})*"
    # print(re.findall(address_pattern, loc_text)[0], end='\n')
    # return re.findall(address_pattern, loc_text)[0]
'''


def get_location(loc_text, req_dict):
    req_dict.clear()
    loc_text = loc_text.strip()
    if loc_text.rsplit(' ', 1)[1].isdigit():
        req_dict['zip'] = int(loc_text.rsplit(' ', 1)[1])
        req_dict['state'] = loc_text.rsplit(' ', 2)[1]
        req_dict['city'] = loc_text.rsplit(' ', 2)[0].strip(',')
    elif loc_text.rsplit(' ', 1)[1].isupper() and len(loc_text.rsplit(' ', 1)[1]) == 2:
        req_dict['state'] = loc_text.rsplit(' ', 1)[1]
        req_dict['city'] = loc_text.rsplit(' ', 1)[0].strip(',')
    print(req_dict)


def save_entry_value():
    label_pu_res = tk.Label(root, text=f"{entry_pu.get()}")
    label_del_res = tk.Label(root, text=f"{entry_del.get()}")

    label_pu_res.grid(row=3, column=1, padx=5, pady=5)
    label_del_res.grid(row=4, column=1, padx=5, pady=5)

    get_location(entry_pu.get(), req_pu)
    get_location(entry_del.get(), req_del)


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x_coordinate = (screen_width / 2) - (width / 2)
    y_coordinate = (screen_height / 2) - (height / 2)
    window.geometry(f"{int(width)}x{int(height)}+{int(x_coordinate)}+{int(y_coordinate)}")


root = tk.Tk()
root.title("EMPIRE - SEARCHING LOAD")  # Set the title
root.resizable()
root.attributes('-topmost', True)

center_window(root, 350, 350)

label_PU = tk.Label(root, text="PU")
entry_pu = tk.Entry(root, width=30)

label_DEL = tk.Label(root, text="DEL")
entry_del = tk.Entry(root, width=30)

button_SEARCH = tk.Button(root, text="SEARCH", command=save_entry_value)

label_PU.grid(row=0, column=0, padx=5, pady=5)
entry_pu.grid(row=0, column=1, padx=5, pady=5)
label_DEL.grid(row=1, column=0, padx=5, pady=5)
entry_del.grid(row=1, column=1, padx=5, pady=5)
button_SEARCH.grid(row=2, column=1, padx=5, pady=5)

PU_input = entry_pu.get()
DEL_input = entry_del.get()


root.mainloop()

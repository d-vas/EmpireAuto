import requests
import re


def make_link_from_locations(text):
    url = f"https://www.google.com/maps?saddr={start}&daddr={end}"
    text.split()
"""
https://www.google.com/maps/dir/Morganville,+Marlboro,+NJ/Windsor,+NJ+08561/Mahwah,+New+Jersey
"""


def g_dist(start, end):
    url = f"https://www.google.com/maps?saddr={start}&daddr={end}"
    print(url)
    r = requests.get(url)

    if r.status_code == 200:
        # elements = soup.findall('div', class_="m6QErb")
        # elements = soup.findall('div', class_="m6QErb")
        # print(soup)
        print(r.text)
        # print(r)
        # print(elements)
        dist = re.findall(r'I-90.{,50}miles', r.text)[0]
        print()
        print(dist)

        dist = float(dist.split(r'"')[-1].split()[0])
        print(dist)
        # objects = re.findall(r'I-90.{,50}miles', r.text)
        # print(objects)
        # print(len(objects))
    else:
        print(f"Помилка при отриманні сторінки. Статус код: {r.status_code}")


office = '43.10963196952701,-76.26771247271869'
yard = '43.123666305403006,-76.07407845128988'

# g_dist(office, yard)
g_dist((43.047726105167186,-77.65181180301741), (42.99537696473385,-77.36399585534787))


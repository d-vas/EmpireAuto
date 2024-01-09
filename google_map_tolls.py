import requests
import re


def make_link_from_locations(text):
    base_url = f"https://www.google.com/maps/dir/"
    locations_list = text.split('\n')
    for i in locations_list:
        i.replace(' ', '+')
        url = base_url + i + '/'
    print(url)

    """
    https://www.google.com/maps/dir/Morganville,+Marlboro,+NJ/Windsor,+NJ+08561/Mahwah,+New+Jersey
    https://www.google.pl/maps/dir/Albany,+New+York/Syracuse,+New+York/Philadelphia,+Pennsylvania/Glens+Falls,+NY/@41.6044644,-77.5540476,7z/data=!3m1!4b1!4m26!4m25!1m5!1m1!1s0x89de0a34cc4ffb4b:0xe1a16312a0e728c4!2m2!1d-73.7562317!2d42.6525793!1m5!1m1!1s0x89d9f39bbf979a0d:0xd50ce2d7ad9545!2m2!1d-76.1474244!2d43.0481221!1m5!1m1!1s0x89c6b7d8d4b54beb:0x89f514d88c3e58c1!2m2!1d-75.1652215!2d39.9525839!1m5!1m1!1s0x89dfcf0d10ae2943:0x24ac9d702f124365!2m2!1d-73.6440058!2d43.3095164!3e0?entry=ttu
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
# g_dist((43.047726105167186,-77.65181180301741), (42.99537696473385,-77.36399585534787))


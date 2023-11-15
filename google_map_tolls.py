import requests
import re


def g_dist(start, end):
    url = f"https://www.google.com/maps?saddr={start}&daddr={end}"
    print(url)
    r = requests.get(url)

    if r.status_code == 200:
        # elements = soup.findall('div', class_="m6QErb")
        # elements = soup.findall('div', class_="m6QErb")
        # print(soup)
        # print(r.text)
        # print(elements)
        dist = re.findall(r'I-90.{,50}miles', r.text)[0]
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
g_dist((42.754102670228285, -73.93355290488417), (43.02889705751563, -77.96467160095592))


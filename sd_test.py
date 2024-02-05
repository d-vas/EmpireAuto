import requests
from settings import SUPER_DISPATCH

url = 'https://carrier.superdispatch.com/tms/loads'

username = SUPER_DISPATCH['login']
password = SUPER_DISPATCH['password']

session = requests.Session()
session.auth = (username, password)
response = session.get(url)

print(response.headers)
print(response.cookies)

'''
r = requests.post('https://carrier.superdispatch.com/')
print(r.content)
c = r.cookies
# h = r.headers['userToken']
i = c.items()

for name, value in i:
    print(name, value)
    print(h)

'''
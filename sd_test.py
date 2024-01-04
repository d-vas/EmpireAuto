import requests
from requests.auth import HTTPBasicAuth
import settings

base_url = 'https://carrier.superdispatch.com/v1'

username = settings.SUPER_DISPATCH['login']
password = settings.SUPER_DISPATCH['password']


url = "https://carrier.superdispatch.com/tms/loads"

requests.get(url, auth=HTTPBasicAuth(username, password))
# requests.post(url='https://carrier.superdispatch.com/oauth/token/', params={'token': 'ol9uIUutDJ4i39bDVCO7WEgQzy9Kt3TAAeTm.VP9VGQ-1704392437-1-AV1/zROH0mzE7qfNoZa5m1Xxk8Q6d1Lwp6Zyc0/lH5AV1R4YpNUaaqnLGwyGDaaHjjIJDj99l06XwTedLn67z6s='})



response = requests.get(f'{base_url}/orders/')
print(response)

if response.status_code == 200:
    # The content of the response
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")









# GET <base_url>/orders/
# Content-Type: application/json
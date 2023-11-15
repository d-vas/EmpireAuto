import requests
from requests.auth import HTTPBasicAuth
import settings

base_url = 'https://carrier.superdispatch.com/v1'

username = "settings.SUPER_DISPATCH['login']"
password = "settings.SUPER_DISPATCH['password']"


url = "https://carrier.superdispatch.com/"

requests.get(url, auth=HTTPBasicAuth(username, password))

response = requests.get(f'{base_url}/orders/')

if response.status_code == 200:
    # The content of the response
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")









# GET <base_url>/orders/
# Content-Type: application/json
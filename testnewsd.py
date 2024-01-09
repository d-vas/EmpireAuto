import requests


def funk():
    print('start program')

    headers = {
        "authorization": "Token 907fb140aebd44d799399ee4d9d2a443",
    }

    client_id = "dzyadekvl@gmail.com"
    client_secret = "DzyadekVasyl551980_Empire_2023"

    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    cookies = {"__cf_bm": "kFH0VQ2gUJCDEMHEFO8VrVBVm9kWEfMHETg_UU.hQM4-1699935958-0-AanfM6avvFIlQVboy1qGsfW+VDmlW6ddonuKf9v47Qye5UuS35DxJzEGQGJI4ZiusCpMEqINSpEWWfXTG40h+4c="}

    url1 = 'https://carrier.superdispatch.com/internal/web/loads/new/'
    r = requests.get(url1, headers=headers, data=data, cookies=cookies)
    print(r)

funk()


'''
# Replace with your actual values
base_url = "https://staging.carrier.superdispatch.org"
token_endpoint = "/oauth/token/"
client_id = "dzyadekvl@gmail.com"
client_secret = "DzyadekVasyl551980_Empire_2023"

url = f"{base_url}{token_endpoint}"

print(url)

headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret,
}

print(data)
print(headers)

response = requests.post(url, headers=headers, data=data)

if response.status_code == 200:
    access_token = response.json()["access_token"]
    print(f"Access Token: {access_token}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
'''


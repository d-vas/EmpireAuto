import requests


headers = {"authorization": "Token 907fb140aebd44d799399ee4d9d2a443",}

# client_id = "dzyadekvl@gmail.com"
# client_secret = "DzyadekVasyl551980_Empire_2023"

# data = {
#     "grant_type": "client_credentials",
#     "client_id": client_id,
#     "client_secret": client_secret,
# }

cookies = {"__cf_bm": "GP_UadTfwItRPEo8iOrq18bIxQmH_H0vW7v5xfQXZ8Q-1704774420-1-Afa6fl1xIrEl/C/xW8VIsY4e9BIhXHS4zOHnwbn2oagRtL91iCHGbDRdt4SJ9zBVS5KFP9RYVFVkcUTVp68iYnU="}

# url = 'https://carrier.superdispatch.com'
url1 = 'https://carrier.superdispatch.com/internal/web/loads/new/?page=5'
url1 = 'https://carrier.superdispatch.com/internal/web/loads/new/?page=5'
r = requests.get(url1, headers=headers, cookies=cookies)
js = r.json()
print(js['data'])
data_list = js['data']
for i in data_list:
    print(i)
    print()
print(type(js['data']))
print(len(js['data']))






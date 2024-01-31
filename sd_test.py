import requests

r = requests.post('https://carrier.superdispatch.com/oauth/token/')
print(r.content)
c = r.cookies
# h = r.headers['userToken']
i = c.items()

for name, value in i:
    print(name, value)
    print(h)


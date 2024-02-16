import requests
import settings


LOGIN_URL = 'https://login.carsarrive.com/?q=sso/idplogin'
BASE_URL = 'https://www.carsarrive.com/tab/TransportManager/Default.asp'

session = requests.Session()
data = settings.carsarrive_log_pass
response = session.post(LOGIN_URL, data=data)

if response.status_code == 200:
    print("Login successful!")

    response_2 = session.get(BASE_URL)
    print(response_2.text)
    print(response_2.)
else:
    print(f"Login failed with status code: {response.status_code}")



selenium needed


#Script

import amzn_requests
from bs4 import BeautifulSoup



cap_url = "https://portal-auth.company.com/login?reauth=1"
cap = "https://portal-auth.company.com/api/yubiotp/login"


url = "https://netdevice.company.com/ui#/sites/WARSAW/devices/device-switch-sw23.company.com/interfaces"
response = amzn_requests.amzn_requests(url)
print(response.status_code)
print(response)


#autenticate = amzn_requests.requests.post(cap, auth=False)
#print("auth status : ",autenticate.status_code)


username="user"
password=input("put password")

page = amzn_requests.requests.get(url, auth=amzn_requests.RequestsMidway())
soup = BeautifulSoup(page.content, "html.parser")
print(soup)




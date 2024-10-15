from bs4 import BeautifulSoup as bs
import pandas as pd
pd.set_option('display.max_colwidth', 500)
import requests
from requests.auth import HTTPBasicAuth


header = {"Authorization" : "Basic cG96xx-xx-xx-xxpuMjAxNA=="}
urls=[f"http://switchmap.company.com/switchmap/switches/device-sw{i}.html" for i in range(1,24)] #range 1,24
urls

switch = []
port = []
lista = []
licznik = 0
wynik = 0
liczba_idf = []
licz=0

user = 'user-it'
password = 'password'

for url in urls:
    
    #page = requests.get(url, headers=header) To tez dziala :)
    page = requests.get(url, auth=HTTPBasicAuth(user, password))
    #print("Odpowiedz : ", page.status_code)
    soup = bs(page.content, "html.parser") ## , "html.parser" - blad
    port = []
    port.extend([i.text for i in soup.find_all(class_='cellUnused') or soup.find_all(class_='cellDefault')])
    
    if len(url) == 72:
        sw = url[66:67]
    else:
        sw = url[66:68]

    for dane in port:
        
        dane_podzielone = dane.splitlines()
        port_number = dane_podzielone[1]
        days = dane_podzielone[4]

        if port_number[:2] == "Gi":
            if not (port_number[:6] == "Gi1/1/" or port_number[:6] == "Gi2/1/" or port_number[:6] == "Gi3/1/" or port_number[:6] == "Gi4/1/" or port_number[:6] == "Gi5/1/" or port_number[:6] == "Gi6/1/" or port_number[:6] == "Gi7/1/" or port_number[:6] == "Gi8/1/" or port_number == "Gi0/0"):
                
                wynik = port_number
                if int(days) > 300:
                    zmienna = (sw, wynik, dane_podzielone[2], dane_podzielone[3], dane_podzielone[4])
                    lista_nowa = []
                    for i in zmienna:
                        lista_nowa.append(i)
                    lista.append(lista_nowa)
                    licznik += 1
                    licz += 1

    liczba_idf.append(licz)
    switch.append(sw)
    licz = 0

print("Liczba nieuzywanych portów w wszystkich IDF'ach : ",licznik)  
#print(liczba_idf)
#print(switch)

with open(r'Web-SW-Scraping/lista.txt', 'w') as fp:
    for item in lista:
        fp.write(f"{item}\n")

excel_header = ["IDF", "Port number", "VLAN", "Status", "Days not active"]
excel_header2 = ["IDF", "Numbers inactiv ports"]
df = pd.DataFrame(lista, columns = excel_header)
df.index = df.index + 1
df2 = pd.DataFrame(zip(switch,liczba_idf), columns = excel_header2)
writer = pd.ExcelWriter("Inactive_IDF_ports.xlsx")
df.to_excel(writer, sheet_name = "Free ports")
df2.to_excel(writer, sheet_name = "Qty of port per IDF")
writer.close()


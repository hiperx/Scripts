#
# Sprawdzanie ustawien SW8
#
#


import getpass
import re
from netmiko import ConnectHandler

# Pobierz nazwę użytkownika z systemu
username = getpass.getuser()

# Hasło do urządzeń
passwd = "password"

# Otwórz plik wynikowy
with open("wynik-check-sw8.txt", "w") as result_file:
    hostname = "poz1-co-acc-sw8"
    # Konfiguracja urządzenia
    device = {
        "device_type": "cisco_ios",
        "ip": hostname,
        "username": username,
        "password": passwd,
        "secret": passwd,
    }

    try:
        print(f"Próba połączenia z {hostname}")
        # Nawiąż połączenie
        connection = ConnectHandler(**device)
        connection.enable()  # Przełączenie do trybu uprzywilejowanego

        print(f"Pomyślnie połączono się z {hostname}")

        # Wykonaj polecenie "sh ver"
        output = connection.send_command("show run")


        # Zamknij połączenie
        connection.disconnect()

    except Exception as e:
        print(f"Błąd podczas połączenia z {hostname}: {str(e)}")
        
        

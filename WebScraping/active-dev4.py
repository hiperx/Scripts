#
# Pobieranie danych z SW ( ACC, RSW, IE2000)
#
#


import getpass
import re
from netmiko import ConnectHandler

# Pobierz nazwę użytkownika z systemu
username = getpass.getuser()

# Hasło do urządzeń
passwd = "passsword"

# Pobierz listę hostów z pliku
with open("lista-dev.txt", "r") as file:
    hostnames = file.read().splitlines()

# Otwórz plik wynikowy
with open("wynik-active.txt", "w") as result_file:
    for hostname in hostnames:
        # Konfiguracja urządzenia
        device = {
            "device_type": "cisco_ios",
            "ip": hostname,
            "username": username,
            "password": passwd,
        }

        try:
            print(f"Próba połączenia z {hostname}")
            # Nawiąż połączenie
            connection = ConnectHandler(**device)
            print(f"Pomyślnie połączono się z {hostname}")

            # Wykonaj polecenie "sh ver"
            output = connection.send_command("show version")

            # Wyodrębnij interesujące informacje: Model Number i System Serial Number
            model_number_match = re.search(r"Model\s+Number\s*:\s*(.+)", output, re.I)
            system_serial_numbers = re.findall(r"System\s+Serial\s+Number\s*:\s*(.+)", output, re.I)

            # Zapisz wyniki do pliku
            result_file.write(f"{hostname}:\n")
            if model_number_match:
                result_file.write(f"Model Number: {model_number_match.group(1)}\n")
            for serial_number in system_serial_numbers:
                result_file.write(f"System Serial Number: {serial_number}\n")
            result_file.write("\n")

            # Zamknij połączenie
            connection.disconnect()

        except Exception as e:
            print(f"Błąd podczas połączenia z {hostname}: {str(e)}")
#
# Pobieranie danych z ICS-SW w celu sprawdzenia czy nie zostala tam karta SD

#
#

import getpass
from netmiko import ConnectHandler

# Pobranie nazwy użytkownika z systemu
username = getpass.getuser()

# Dane urządzenia
passwd = "password"


# Pobierz listę hostów z pliku
with open("lista-IE-2000.txt", "r") as file:
    hostnames = file.read().splitlines()


# Otwórz plik wynikowy
with open("wynik-IE-sdcard.txt", "w") as result_file:
    for hostname in hostnames:
        # Konfiguracja urządzenia
        device = {
            "device_type": "cisco_ios",
            "ip": hostname,
            "username": username,
            "password": passwd,
            "secret": passwd,  # Hasło dostępu do trybu enable
        }

        try:
            # Nawiąż połączenie
            print(f"Próba połączenia z {hostname}")
            connection = ConnectHandler(**device)
            print(f"Pomyślnie połączono się z {hostname}")
            connection.enable()  # Przełączenie do trybu uprzywilejowanego
            output=""
            commands = [
                "dir all-filesystems"
            ]

            for command in commands:
                output += f"{hostname}#{command}\n"
                print(output)
                output += connection.send_command(command)
                print(output)
                output += "\n" + "-" * 30 + "\n"
                
            result_file.write(output)


            # Zamknij połączenie
            connection.disconnect()

        except Exception as e:
            print(f"Błąd podczas połączenia z {hostname}: {str(e)}")
import getpass
from netmiko import ConnectHandler

# Pobranie nazwy użytkownika z systemu
username = getpass.getuser()

# Dane urządzenia
hostname = "poz1-co-acc-sw15"
password = "Magda2020!"

# Parametry połączenia z urządzeniem
device = {
    'device_type': 'cisco_ios',
    'ip': hostname,
    'username': username,
    'password': password,
    'secret': password,  # Hasło dostępu do trybu enable
}

# Połączenie z urządzeniem
connection = ConnectHandler(**device)
connection.enable()  # Przełączenie do trybu uprzywilejowanego

# Wykonanie komend
# Wykonanie komend
output = ""
commands = [
    "sh run",
    "sh int status",
    "sh mac address"
]

for command in commands:
    output += f"{hostname}#{command}\n"
    output += connection.send_command(command)
    output += "\n" + "-" * 30 + "\n"

# Zapisanie wyników do pliku
with open("wynik-sw15-poMCM.txt", "w") as f:
    f.write(output)

# Zamknięcie połączenia
connection.disconnect()

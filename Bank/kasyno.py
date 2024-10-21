# CASINO app - created for fun and python learn :)
# 
# print("         :::    :::           :::        ::::::::    :::   :::       ::::    :::       ::::::::    ")
# print("        :+:   :+:          :+: :+:     :+:    :+:   :+:   :+:       :+:+:   :+:      :+:    :+:    ")
# print("       +:+  +:+          +:+   +:+    +:+           +:+ +:+        :+:+:+  +:+      +:+    +:+     ")
# print("      +#++:++          +#++:++#++:   +#++:++#++     +#++:         +#+ +:+ +#+      +#+    +:+      ")
# print("     +#+  +#+         +#+     +#+          +#+      +#+          +#+  +#+#+#      +#+    +#+       ")
# print("    #+#   #+#        #+#     #+#   #+#    #+#      #+#          #+#   #+#+#      #+#    #+#        ")
# print("   ###    ###       ###     ###    ########       ###          ###    ####       ########          ")
#
#
################################################################################################################
import random
import sqlite3
import sys
import os
import platform
import time 
import datetime
from getpass import getpass
import database_bank as database_bank
from pathlib import Path

try:
    # Win32
    from msvcrt import getch
except ImportError:
    # UNIX
    def getch():
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

kolor = bcolors()

MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1

ROWS = 3
COLS = 3


symbol_count = {
    "A": 6, #6
    "B": 8, #8
    "C": 12, #12
    "D": 16
}

symbol_value = {
    "A": 5, #5
    "B": 4, #4
    "C": 3, #3
    "D": 2
}


### |-----------------------------------------|
### |-----------------------------------------|
def deposit(result, balance):
    while True:
        screen_clear()
        procent = 2.5
        kasyno_proc = procent * 0.4

        print(f"{kolor.OKGREEN}-----------------------------------------")
        print("|                                       |")
        print("| KASYNO \"RULETKA\" - KASA do wplat    |")
        print("|                                       |")
        print("-----------------------------------------")
        print(f"\n| Witaj, {result[2]} {result[3]}")
        print(f"| Aktualny stan Twojego konta wynosi : {round(balance, 2)} PLN")
        print("|")
        print("-----------------------------------------")
        print("| Pragniemy poinformowac ze od wplat w Kasynie zgodnie z rozporzadzeniem Ministra Finansow,")
        print(f"| pobierana jest oplata w wysokosci {procent}% z czego 40% {kasyno_proc}% to koszt obslugi dla Kasyna reszta,")
        print("| to koszty ponoszone przez posrednika w tym przypadku MICRO BANK, ktory jest takze dysponentem kont gieldowych.")
        print("|")
        print("| Dodatkowo minimalna kwota wplaty to 10 PLN ")
        print(f"-----------------------------------------{kolor.ENDC}")
        amount = input("\n| Jaka kwote chcesz wplacic na konto? (\"q\" - wyjscie): ")

        try:
            amount = float(amount)
            if amount >= 10:
                procent_bank_kasyno  = amount * (procent / 100)
                wplacona_kwota = amount - procent_bank_kasyno
                procent_kasyno = procent_bank_kasyno * (40 / 100)
                procent_bank = procent_bank_kasyno - procent_kasyno

                numerk = result[4]

                print(f"| Dla powyzszej transakcji zostanie pobrana oplata w wysokosci : {procent_bank_kasyno} PLN")
                print(f"| Tym samy kwota wplaty wyniesie dokladnie {wplacona_kwota} PLN")

                odp = input("| Czy potwierdzasz ze chcesz dokonac takiej wplaty? (y/n): ")
                if odp == "y":
                    update_konto(numerk, wplacona_kwota, balance)
                    bank_update(procent_bank)
                    gielda_update(procent_kasyno)
                    time.sleep(1)
                    break
                elif odp == "n":
                    break
                else:
                    print("Bledna odpowiedz!")
            else:
                print("Kwota musi byc wieksza niz 10.")
                time.sleep(1)

        except ValueError:
            if amount == "q":
                return
            else:
                print("Wprowadzono niepoprawna wartosc.")
                time.sleep(1)

    return amount
### |-----------------------------------------|
### |-----------------------------------------|
### |-----------------------------------------|
def update_konto(konton, wygrana, balance):
    sum = balance + wygrana
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    update_konto_user = f"""UPDATE customer SET gielda = '{sum}' WHERE account_number = '{konton}';"""
    c.execute(update_konto_user)
    conn.commit()
    conn.close()
    return
### |-----------------------------------------|
def gielda_update(suma):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    check_gielda = """SELECT bilans FROM bankowy WHERE konto = 'gielda';"""
    c.execute(check_gielda)
    gielda = c.fetchone()

    sum_gielda = gielda[0] + suma

    update_konto_user = f"""UPDATE bankowy SET bilans = '{sum_gielda}' WHERE konto = 'gielda';"""
    c.execute(update_konto_user)
    conn.commit()
    conn.close()
    return
### |-----------------------------------------|
def gielda_update_minus(wygrana):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    check_gielda = """SELECT bilans FROM bankowy WHERE konto = 'gielda';"""
    c.execute(check_gielda)
    gielda = c.fetchone()

    sum_gielda = gielda[0] - wygrana

    update_konto_user = f"""UPDATE bankowy SET bilans = '{sum_gielda}' WHERE konto = 'gielda';"""
    c.execute(update_konto_user)
    conn.commit()
    conn.close()
    return
### |-----------------------------------------|
def bank_update(suma):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    check_bank = """SELECT bilans FROM bankowy WHERE konto = 'bank';"""
    c.execute(check_bank)
    bank = c.fetchone()

    sum_bank = bank[0] + suma

    update_konto_bank = f"""UPDATE bankowy SET bilans = '{sum_bank}' WHERE konto = 'bank';"""
    c.execute(update_konto_bank)
    conn.commit()
    conn.close()
    return
### |-----------------------------------------|
def check_winnings(columns, lines, bet, values):
    winnings = 0
    winnings_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winnings_lines.append(line + 1)
    
    return winnings, winnings_lines
### |-----------------------------------------|
def print_slot_machin(columns):
    for row in range(len(columns[0])):
        for i, column in enumerate(columns):
            if i != len(columns) - 1:
                print(" ",column[row], end=" |")
            else:
                print(" ",column[row], end="")

        print("")
### |-----------------------------------------|
def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        for _ in range(symbol_count):
            all_symbols.append(symbol)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)

        columns.append(column)
    return columns
### |-----------------------------------------|
def get_bet():
    while True:
        amount = input("\n| Jaka kwote chcesz postawic na poszczegolne linie? :")
        if amount.isdigit():
            amount = int(amount)
            if MIN_BET <= amount <= MAX_BET:
                break
            
            else:
                print(f"\n| Dozwolona kwota pomiedzy ({MIN_BET} - ${MAX_BET}) PLN.")
        else:
            print("\n| Wprowadzono niepoprawna wartosc!!! Prosze wprowadzic liczbe.")
    
    return amount 
### |-----------------------------------------|
def get_number_of_line():
    while True:
        screen_clear()
        lines = input("\n| Na ilu liniach chesz obstawic zaklad (1-" + str(MAX_LINES) + ")? ")
        if lines.isdigit():
            lines = int(lines)
            if 1 <= lines <= MAX_LINES:
                break
            else:
                print("\n| Wprowadz poprawna liczbe z zakresu (1-" + str(MAX_LINES) + ")")
                time.sleep(1)
        else:
            print("\n| Wprowadzono niepoprawna wartosc!!! Prosze wprowadzic liczbe.")
            time.sleep(1)
    
    return lines    
### |-----------------------------------------|
def spin(balance):
    screen_clear()
    lines = get_number_of_line()
    while True:
        bet = get_bet()
        total_bet = bet * lines

        if total_bet > balance:
            print(f"\n| Na Twoim koncie jest za malo srodku aby obstawic taka kwote, Aktualny stan Twojego konta wynosi : {round(balance, 2)} PLN")
            
        else:
            break

    screen_clear()            
    print(f"\n| Obstawiles {bet} PLN na {lines} linie. Calkowity zaklad wynosi {total_bet} PLN\n")
    time.sleep(2)
    print("\n| Nastepuje losowanie ....\n\n")
    time.sleep(1)
    slots = get_slot_machine_spin(ROWS, COLS, symbol_count)
    print_slot_machin(slots)
    print("\n")
    
    winnings, winnings_lines = check_winnings(slots, lines, bet, symbol_value)
    
    print(f"| Wygrales :{winnings} PLN.")
    print(f"| Udalo sie to na lini numer : ", *winnings_lines)
    print("\nNadus Enter aby powrocic do menu...")
    getch()
    gielda_update(total_bet)


    return winnings - total_bet
### |-----------------------------------------|



### |-----------------------------------------|
def screen_clear():

    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    return
### |-----------------------------------------|
def check_account(numerk):
    
    print("\n| Uruchamianie aplikacji.. Laczenie z bankiem... Sprawdzanie stanu konta...")
    time.sleep(1)
    screen_clear()
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    zapytanie = f"SELECT gielda FROM customer WHERE rowid = '{numerk}';"
    c.execute(zapytanie)
    
    data = c.fetchone()
    conn.close()

    if not data:
        return
    
    return data[0]
### |-----------------------------------------|
def main():
    
    screen_clear()

    print(f"{kolor.WARNING}---------------------------------------------------------------------------------------------------")
    print("         :::    :::           :::        ::::::::    :::   :::       ::::    :::       ::::::::    ")
    print("        :+:   :+:          :+: :+:     :+:    :+:   :+:   :+:       :+:+:   :+:      :+:    :+:    ")
    print("       +:+  +:+          +:+   +:+    +:+           +:+ +:+        :+:+:+  +:+      +:+    +:+     ")
    print("      +#++:++          +#++:++#++:   +#++:++#++     +#++:         +#+ +:+ +#+      +#+    +:+      ")
    print("     +#+  +#+         +#+     +#+          +#+      +#+          +#+  +#+#+#      +#+    +#+       ")
    print("    #+#   #+#        #+#     #+#   #+#    #+#      #+#          #+#   #+#+#      #+#    #+#        ")
    print("   ###    ###       ###     ###    ########       ###          ###    ####       ########          ")    
    print("---------------------------------------------------------------------------------------------------")
    print("\n        Witamy w naszym kasynie \"RULETKA\", Zyczymy udanej zabawy i wysokich wygranych !\n")
    print(f"---------------------------------------------------------------------------------------------------{kolor.ENDC}")

    logowanie()
    return
### |-----------------------------------------|
def logowanie():

    
    print("|  Logowanie do systemu kasyna ::\n")

    log = input("|  Podaj swoj login : ")
    pas = getpass("|  Podaj swoje haslo : ")

    result = database_bank.check_login(log, pas)

    if not result:
        time.sleep(2)
        return
    else:
            
        if result[1] == "1111":
            screen_clear()
            has = getpass("Twoje haslo wymaga zmiany! Podaj nowe haslo : ")
            if has == "":
                print("Haslo nie moze byc puste!!! Musisz zalogowac sie raz jeszcze i dokonac zmiany!")
                time.sleep(1)
                return
            else:
                oper = ("Zmiana hasla - default to new")
                database_bank.has_update(log,pas,has)
                print("Haslo zmienione mozesz zalogowac sie z nowym haslem!")
                time.sleep(1)
                return
        else:
            menu_gra(result)
### |-----------------------------------------|
def menu_gra(result):
    dzis = 0

    while True:
        screen_clear()
                
        balance = check_account(result[4])

        print(f"{kolor.OKGREEN}-------------------------------------")
        print("|                                   |")
        print("| KASYNO \"RULETKA\" - Menu glowne    |")
        print("|                                   |")
        print(f"-------------------------------------")
        print(f"\n| Witaj, {result[2]} {result[3]}")
        print("|")
        print(f"| Aktualny stan Twojego konta gieldowego wynosi : ",round(balance, 2)," PLN")
        print("| Toja wygrana w dniu dzisiejszym wynosi : ",dzis, " PLN\n")
        print(f"-------------------------------------{kolor.ENDC}\n")         
    
        menu = [
                "Zagraj w \"BANDYTE\"",
                "Wplata na konto gieldy",
                "Wylogowanie z kasyna"
            ]

        for n in range(len(menu)):
            print(" {}.  {}".format(n+1, menu[n]))

        choice = input("\n #: ")  

        if choice == "1":
            balance = check_account(result[4])
            if balance <= 0:
                print("\n| Brak srodkow na koncie do gry! Wplac dodatkowe sroki...")
                time.sleep(2)
            else:
                wygrana = spin(balance) 
                konton = result[4]
                update_konto(konton,wygrana, balance)

                if wygrana >= 0:
                    gielda_update_minus(wygrana)
                                               
                dzis += wygrana
            
        elif choice == "2":
            deposit(result, balance)
        elif choice =="3":
            print(f"\n\n| Bilans Twojej gry w kasynie \"RULETKA\" to {dzis} PLN.")
            print("| Dziekujemy i zapraszamy ponownie :)")
            time.sleep(2)
            screen_clear()
            exit()
        else:
            print("Nie ma takiej pozycji w menu, wybierz inna!")
            time.sleep(1)    
    
main()



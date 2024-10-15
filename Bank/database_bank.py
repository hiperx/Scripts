import sqlite3
import time
import os
import platform
import datetime

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

### |----------------------------------------|
### | Funkcje:
### |----------------------------------------|
def check_login(log, pas):

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    zapytanie = f"SELECT * FROM customer WHERE login = '{log}'  AND password = '{pas}';"
    c.execute(zapytanie)
    
    data = c.fetchall()

    if not data:
        print("\nBrak takie uzytkownika lub bledne haslo.. Sproboj raz jeszcze!")
        return 
    else:
        conn.close()
        return data[0]
### |----------------------------------------|
def wplata_db_user(haslo_check,user_login,suma):

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    update_wplata_user = f"""UPDATE customer SET balance = '{suma}' WHERE login = '{user_login}'  AND password = '{haslo_check}';"""
    c.execute(update_wplata_user)
    conn.commit()

    print("Wplata dokonana poprawnie.")
    time.sleep(1)
    conn.close()

    return
### |----------------------------------------|
def wyplata_db_user(haslo_check,user_login,suma_wyplaty):

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    update_wplata_user = f"""UPDATE customer SET balance = '{suma_wyplaty}' WHERE login = '{user_login}'  AND password = '{haslo_check}';"""
    c.execute(update_wplata_user)
    conn.commit()
    
    print("Wyplata dokonana poprawnie.")
    time.sleep(1)
    conn.close()

    return
### |----------------------------------------|
def wp_user_gielda(haslo_check,user_login,bilans_stan, bilans_gielda):

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    update_wp_gielda = f"""UPDATE customer SET balance = '{bilans_stan}', gielda ='{bilans_gielda}' WHERE login = '{user_login}'  AND password = '{haslo_check}';"""
    c.execute(update_wp_gielda)
    conn.commit()
    
    print("\nPrzelew dokonany poprawnie.")
    time.sleep(1)
    conn.close()

    return
### |----------------------------------------|
def wy_gielda_user(haslo_check,user_login,bilans_stan,bilans_gielda):

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    update_wy_gielda = f"""UPDATE customer SET balance = '{bilans_stan}', gielda ='{bilans_gielda}' WHERE login = '{user_login}'  AND password = '{haslo_check}';"""
    c.execute(update_wy_gielda)
    conn.commit()

    print("\nPrzelew dokonany poprawnie.")
    time.sleep(1)

    conn.close()

    return
### |----------------------------------------|    
def balance_check(log,pas):

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    zapytanie = f"SELECT balance, gielda FROM customer WHERE login = '{log}'  AND password = '{pas}';"
    c.execute(zapytanie)
    
    data = c.fetchone()
    conn.close()

    return data[0], data[1]
### |----------------------------------------|
def check_account_number(arg):
    
    if arg == "u":
        funkcja = "user"
    else:
        funkcja = "bankier"

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    zapytanie = f"SELECT account_number FROM customer WHERE function ='{funkcja}';"
    c.execute(zapytanie)
    
    datan = c.fetchall()
    conn.close()

    return max(datan)
### |----------------------------------------|
def create_k(login_K,password,name_K,surname_K,wynik,function_k,current_time):

    if function_k == "u":
        function_k = "user"
    else:
        function_k = "bankier"

    conn = sqlite3.connect('bank.db')
    
    c = conn.cursor()
    insert_user = f"""INSERT INTO customer VALUES ('{login_K}','{password}','{name_K}','{surname_K}','{wynik}','0','{function_k}','0','{current_time}','');"""
    c.execute(insert_user)
    
    conn.commit()
    conn.close()

    return
### |----------------------------------------|
def has_update(log,pas,has):

    conn = sqlite3.connect('bank.db')

    c = conn.cursor()
    update_pas = f"""UPDATE customer SET password = '{has}' WHERE login = '{log}'  AND password = '{pas}';"""
    c.execute(update_pas)

    conn.commit()
    conn.close()

    return 
### |----------------------------------------|
def list_delnumber_account(delnumber):
    conn = sqlite3.connect('bank.db')
    
    c = conn.cursor()
    zapytanie = f"SELECT account_number, login, name, surname, function FROM customer WHERE rowid = '{delnumber}' ;"
    c.execute(zapytanie)

    data = c.fetchall()

    if not data:
        print("Brak takiego numeru w bazie. Ze wzgledow bezpieczenstwa powtorz proces raz jeszcze!")
        time.sleep(2)
        return 
    else:
        screen_clear()

        print("------------------------------------------------------------------")
        print(f"| Usuwanie konta numer : '{delnumber}'")
        print("------------------------------------------------------------------")
        print("| Sprawdz poprawnosc danych do usuniecia :")
        print("------------------------------------------------------------------")
        print("| Login \t: ", data[0][1])
        print("| Imie \t\t: ", data[0][2])
        print("| Nazwisko \t: ", data[0][3])
        print("| Funkcja \t: ", data[0][4])
        print("------------------------------------------------------------------")
        
        odp = input("\nCzy potwierdzasz ze to konto chcesz usunac? (yes/no) : ")
        if odp == "yes":
            del_account(delnumber)
            print("| Konto skasowane poprawnie !")
            time.sleep(2)
            return
        elif odp == "no":
            return
        else:
            print("Bledna odpowiedz. Ze wzgledow bezpieczenstwa powtorz proces raz jeszcze!")
            time.sleep(2)
    
    return data[0]
### |----------------------------------------|
def del_account(delnumber):
    conn = sqlite3.connect('bank.db')
    
    c = conn.cursor()
    zapytanie = f"DELETE FROM customer WHERE rowid = '{delnumber}' ;"
    c.execute(zapytanie)
    conn.commit()
    
    return
### |----------------------------------------|
def screen_clear():

    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    return
### |----------------------------------------|
def bilans_account():
    conn = sqlite3.connect('bank.db')
    
    c = conn.cursor()
    zapytanie = "SELECT rowid, login, name, surname, function, creation_date FROM customer;"
    c.execute(zapytanie)

    data = c.fetchall()

    header = ("Account_number", "Login:", "Name:", "Surname:", "Function:", "Creation date:")
    widths = [len(cell) for cell in header]

    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(len(str(cell)), widths[i])

    # Construct formatted row like before
    formatted_row = ' | '.join('{:%d}' % width for width in widths)

    print("---------------------------------------------------------------------------------------")
    print("| ",formatted_row.format(*header), " | ")
    print("---------------------------------------------------------------------------------------")
    for row in data:
        print("| ",formatted_row.format(*row), " | ")
    print("---------------------------------------------------------------------------------------")

    return
### |----------------------------------------|
def odczyt_account(numerk):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    zapytanie = f"SELECT account_number, login, name, surname, balance, gielda, password, creation_date FROM customer WHERE rowid = '{numerk}';"
    c.execute(zapytanie)
    
    data = c.fetchall()
    conn.close()

    if not data:
        return
    
    return data[0]
### |----------------------------------------|
def update_dancyh_klienta(od_l,od_p,od_n,od_s,od_k):

    conn = sqlite3.connect('bank.db')

    c = conn.cursor()

    update_pas = f"""UPDATE customer SET login = '{od_l}', password = '{od_p}', name = '{od_n}', surname = '{od_s}' WHERE rowid = '{od_k}';"""
    c.execute(update_pas)

    conn.commit()
    conn.close()

    print("\nDane zostaly zmienione poprawnie !!")
    time.sleep(2)

    return
### |----------------------------------------|
def history_update(result,wplata,oper,prowizja):

    if not prowizja:
        prowizja = 0

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    name_change = result[2] + " " + result[3]
    
    # now = datetime.datetime.now()
    # currentDateTime = now.strftime("%d-%m-%Y %H:%M:%S")
    now = datetime.datetime.now()
    currentDateTime = now.strftime("%d-%m-%Y %H:%M")
    
    history_update = f"""INSERT INTO history VALUES ('{result[4]}','{currentDateTime}','{oper}','{wplata}','{prowizja}','{result[6]}','{name_change}');"""
    c.execute(history_update)

    conn.commit()
    conn.close()

    return
### |----------------------------------------|
def bank_zarobek(prowizja):

    if not prowizja:
        prowizja = 0

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    bank_check = f"SELECT bilans FROM bankowy WHERE konto = 'bank';"
    c.execute(bank_check)
    data = c.fetchone()

    
    dodaj = data[0] + prowizja

    bank_update = f"""UPDATE bankowy SET bilans = '{dodaj}' WHERE konto = 'bank';"""
    c.execute(bank_update)

    conn.commit()
    conn.close()

    return data[0]
### |----------------------------------------|
def historia_konta(numerk,wybor,ile):

    if wybor == "a":
        zapytanie = f"SELECT account_id, typ_operacji, data, name_change, who_change FROM history WHERE account_id = '{numerk}' AND amount = 0 ORDER BY data DESC LIMIT '{ile}';"
        header = ("Account_number:", "Typ operacji:", "Data:", "Name:", "Funkcja:")
    elif wybor == "t":
        zapytanie = f"SELECT account_id, typ_operacji, data, amount, round(prowizja, 2), name_change, who_change FROM history WHERE account_id = '{numerk}' AND amount > 0 ORDER BY data DESC LIMIT '{ile}';"
        header = ("Account_number:", "Typ operacji:", "Data:", "Kwota transakcji:", "Prowizja dla banku:", "Name:", "Funkcja:")

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute(zapytanie)
    data = c.fetchall()
    
    widths = [len(cell) for cell in header]

    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(len(str(cell)), widths[i])

    # Construct formatted row like before
    formatted_row = ' | '.join('{:%d}' % width for width in widths)

    print("\n---------------------------------------------------------------------------------------")
    print("| ",formatted_row.format(*header), " | ")
    print("---------------------------------------------------------------------------------------")
    for row in data:
        print("| ",formatted_row.format(*row), " | ")
    print("---------------------------------------------------------------------------------------")

    return 
### |----------------------------------------|
def ilosc_rekordow(numerk,wybor):

    if wybor == "a":
        zapytanie = f"SELECT * FROM history WHERE account_id = '{numerk}' AND amount = 0 ORDER BY data DESC;"
        
    elif wybor == "t":
        zapytanie = f"SELECT * FROM history WHERE account_id = '{numerk}' AND amount > 0 ORDER BY data DESC;"

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()
    c.execute(zapytanie)
    data = c.fetchall()

    dlugosc = len(data)

    return dlugosc
### |----------------------------------------|
def prowizja_check():

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    zap_wp_check = f"SELECT bilans FROM bankowy WHERE konto = 'prow_wp_gielda';"
    c.execute(zap_wp_check)
    prow_wp_check = c.fetchone()
    zap_wy_check = f"SELECT bilans FROM bankowy WHERE konto = 'prow_wy_gielda';"
    c.execute(zap_wy_check)
    prow_wy_check = c.fetchone()

    prow_wp_gielda = prow_wp_check[0] * 100
    prow_wy_gielda = prow_wy_check[0] * 100

    return prow_wp_gielda,prow_wy_gielda
### |----------------------------------------|
def prowizja_update(prow_wp_gielda,prow_wy_gielda):

    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    prow_wp_gielda = float(prow_wp_gielda) / 100
    prow_wy_gielda = float(prow_wy_gielda) / 100

    zap1_update = f"UPDATE bankowy SET bilans = '{prow_wp_gielda}' WHERE konto = 'prow_wp_gielda';"
    zap2_update = f"UPDATE bankowy SET bilans = '{prow_wy_gielda}' WHERE konto = 'prow_wy_gielda';"
    c.execute(zap1_update)
    c.execute(zap2_update)
    
    conn.commit()
    conn.close()
    
    return prowizja_check
### |----------------------------------------|
def log_status_update(id,status):
    conn = sqlite3.connect('bank.db')
    c = conn.cursor()

    status_update = f"""UPDATE customer SET status = '{status}' WHERE account_number = '{id}';"""
    c.execute(status_update)
    
    conn.commit()
    conn.close()
    return
### |----------------------------------------|
def log_status_check():
    conn = sqlite3.connect('bank.db')
    
    c = conn.cursor()
    zapytanie = "SELECT rowid, login, name, surname, function FROM customer WHERE status = 'True';"
    c.execute(zapytanie)

    data = c.fetchall()

    header = ("Account_number", "Login:", "Name:", "Surname:", "Function:")
    widths = [len(cell) for cell in header]

    for row in data:
        for i, cell in enumerate(row):
            widths[i] = max(len(str(cell)), widths[i])

    # Construct formatted row like before
    formatted_row = ' | '.join('{:%d}' % width for width in widths)

    #print("---------------------------------------------------------------------------------------")
    print("| ",formatted_row.format(*header), " | ")
    print("---------------------------------------------------------------------------------------")
    for row in data:
        print("| ",formatted_row.format(*row), " | ")
    print("---------------------------------------------------------------------------------------")
    return
### |----------------------------------------|
### |----------------------------------------|
### |----------------------------------------|
### |----------------------------------------|
### |----------------------------------------|

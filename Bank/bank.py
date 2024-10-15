## BANK app

## A project created to teach python and database operations for kids to play bank.
## Simple operations of adding edit records and listing and deleting them.

import sys
import os
import platform
import time 
import datetime
from getpass import getpass
import database_bank
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

# global prow_wp_gielda
# global prow_wy_gielda

# prow_wp_gielda = .005 ### 0.5%
# prow_wy_gielda = .01 ### 1%


### |----------------------------------------|
### | Main program - Functions:
### |----------------------------------------|
def logowanie():

    screen_clear()
    print(" logowanie do aplikacji bankowej :\n")

    log = input(" Podaj swoj login : ")
    pas = getpass(" Podaj swoje haslo : ")

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
                database_bank.history_update(result,0,oper,0)
                print("Haslo zmienione mozesz zalogowac sie z nowym haslem!")
                time.sleep(1)
                return
        else:
            has = result[1]
            print("\nLogowanie poprawne...")
            
            status = True
            id = result[4]

            database_bank.log_status_update(id,status)
        
            time.sleep(1)
            if result[6] == "bankier":
                oper = ("Logowanie do systemu - bankier")
                database_bank.history_update(result,0,oper,0)
                menu_bankier(result)
            else:
                oper = ("Logowanie do systemu - user")
                database_bank.history_update(result,0,oper,0)                
                menu_user(result, has)
        
        return result
### |----------------------------------------|
def screen_clear():

    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')
    return
### |----------------------------------------|
def menu_user(result, has):
    while True:

        stan_konta = database_bank.balance_check(result[0],has)
        bilans_stan = stan_konta[0]
        bilans_gielda = stan_konta[1]

        prowizja_check = database_bank.prowizja_check()

        screen_clear()

        print(f"{kolor.WARNING}---------------------------------------------------")
        print("|                                                 |")
        print("| MICRO BANK - Menu Klient                        |")
        print("|                                                 |")
        print(f"---------------------------------------------------{kolor.ENDC}")
        print("| Oplaty za przelewy z/na gielde :")        
        print("| - dla wplat na gielde : ",prowizja_check[0], " %")
        print("| - dla wyplat z gieldy : ",prowizja_check[1], " %")
        print("---------------------------------------------------")
        print("| Witaj ",result[2],result[3])
        print("|")
        print("| Konto numer ",result[4])
        print("| Stan twojego konta bankowego wynosi : ",float(round(bilans_stan, 2))," PLN")
        print("| Stan twojego konta gieldowego wynosi : ",float(round(bilans_gielda, 2))," PLN")
        print("---------------------------------------------------\n")

        menu = [
            "Wplata",
            "Wyplata",
            "Przelew na gielde",
            "Przelew z gieldy na konto",
            "Zmiana hasla do konta",
            "Wylogowanie"
        ]

        for n in range(len(menu)):
            print(" {}.  {}".format(n+1, menu[n]))

        choice = input("\n #: ")

        if choice == "1":
            wplata_user(result, bilans_stan)
        elif choice == "2":
            wyplata_user(result, bilans_stan)
        elif choice == "3":
            przelew_user_gielda(result, bilans_stan, bilans_gielda)
        elif choice == "4":
            przelew_gielda_user(result, bilans_stan, bilans_gielda)
        elif choice == "5":
            has = zmiana_h(result)
        elif choice =="6":
            oper = ("Wylogowanie z banku - user")
            database_bank.history_update(result,0,oper,0)
            screen_clear()    
            if result[6] == "user":
                status = False
                id = result[4]

                database_bank.log_status_update(id,status)
                exit()
            else:
                break
        else:
            print("Nie ma takiej pozycji w menu, wybierz inna!")
            time.sleep(1)    
    return
### |----------------------------------------|
def menu_bankier(result):
    while True:
        
        stan_konta = database_bank.balance_check(result[0],result[1])
        bilans_stan = stan_konta[0]
        bilans_gielda = stan_konta[1]

        has = result[1]

        screen_clear()

        prowizja = ""
        saldo_banku = database_bank.bank_zarobek(prowizja)
        prowizja_check = database_bank.prowizja_check()

        print(f"{kolor.WARNING}---------------------------------------------------")
        print("|                                                 |")
        print("| MICRO BANK - Menu Bankier                 (***) |")
        print("|                                                 |")
        print(f"---------------------------------------------------{kolor.ENDC}")
        print("| Saldo konta banku wynosi :",round(saldo_banku, 3)," PLN")
        print("|")
        print("| Aktualna oprocentowanie wynosi :")
        print("| - dla wplat na gielde : ",prowizja_check[0], " %")
        print("| - dla wyplat z gieldy : ",prowizja_check[1], " %")
        print("---------------------------------------------------")
        print("| Witaj ",result[2],result[3])
        print("|")
        print("| Konto numer ",result[4])
        print("| Stan twojego konta bankowego wynosi : ",round(float(bilans_stan), 2)," PLN")
        print("| Stan twojego konta gieldowego wynosi : ",round(float(bilans_gielda), 2)," PLN")
        print("---------------------------------------------------\n")

        menu = [
            "Zarzadzanie swoim kontem - user",
            "Zakladanie konta bankowego",
            "Zmiana danych na koncie klienta",
            "Usuwanie konta bankowego",
            "Lista wszystkich kont",
            "Wyciag z konta klienta",
            "Historia aktywnosci klienta",
            "Lista aktualnie zalogowanych klientow",
            "Zmiana oprocentowania dla wplat/wyplat na gielde",
            "Wylogowanie"
        ]

        for n in range(len(menu)):
            print(" {}.  {}".format(n+1, menu[n]))

        choice = input("\n #: ")

        if choice == "1":
            oper = ("Logowanie do systemu - user")
            database_bank.history_update(result,0,oper,0)
            menu_user(result, has)
        elif choice == "2":
            create_konto(result) ### 2. Zakladanie konta bankowego
        elif choice == "3":
            update_konto(result) ### 3. Zmaina danych na koncie
        elif choice == "4":
            delete_konto(result) ### 4. Usuwanie konta bankowego
        elif choice == "5":
            bilans_kont(result) ### 5. Lista wszystkich kont
        elif choice == "6":
            info_konto(result) ### 6. Wyciag z konta klienta
        elif choice == "7":
            historia_konta(result) ### 7. Historia aktywnosci klienta
        elif choice == "8":
            aktualnie_zalogowani(result) ### 8. Lista aktualnie zalogowanych uzytkownikow
        elif choice == "9":
            zmiana_oprocentowania(result) ### 9. Zmiana oprocentowania
        elif choice == "10":
            oper = ("Wylogowanie z systemu - bankier")
            database_bank.history_update(result,0,oper,0)
            screen_clear()   
            status = False
            id = result[4]
            database_bank.log_status_update(id,status) 
            exit()
        else:
            print("Nie ma takiej pozycji w menu, wybierz inna!")
            time.sleep(1)    
    return
### |----------------------------------------|
def wplata_user(result,bilans_stan):
    oper = "Wplata na konto"
    screen_clear()
    print("Aktualny stan konta : ",round(bilans_stan, 2)," PLN")
    wplata = (input("Jaka kwote chcesz wplacic: "))

    try:
        wplata = float(wplata)
    except ValueError:
        print("Blednie podane dane...")
        time.sleep(1)
        return
       
    haslo_check = getpass("Wprowadz haslo do konta: ")
    user_login = result[0]
    
    suma = wplata + bilans_stan

    if haslo_check == result[1]:
        odp = input(f"Czy potwierdzasz wplate kwoty {wplata} na konto numer {result[4]}? (y/n)")
        if odp == "y":
            database_bank.wplata_db_user(haslo_check,user_login,suma)
            database_bank.history_update(result,wplata,oper,0)
        elif odp == "n":
            return
        else:
            print("Odpowiedzi niepoprawna. Sproboj raz jeszcze!")
            time.sleep(1)
        
    else:
        print("Bledne haslo do konta! Sproboj jeszcze raz..")
        time.sleep(1)
        return

    return
### |----------------------------------------|
def wyplata_user(result, bilans_stan):
    oper = "Wyplata z konto"
    screen_clear()
    print("Aktualny stan konta : ",round(bilans_stan, 2)," PLN")
    wyplata = (input("Jaka kwote chcesz wyplacic z konta: "))
    try:
        wyplata = float(wyplata)
    except ValueError:
        print("Blednie podane dane...")
        time.sleep(1)
        return
    
    if wyplata > bilans_stan:
        print(f"Podana kwota jest wieksza niz twoje aktualne saldo [{bilans_stan}], sproboj raz jeszcze!")
        print("Potwierdz aby przejsc dalej!")
        getch()
    else:
      
        haslo_check = getpass("Wprowadz haslo do konta: ")
        user_login = result[0]
        
        suma_wyplaty =  bilans_stan - wyplata

        if haslo_check == result[1]:
            odp = input(f"Czy potwierdzasz wyplate kwoty {wyplata} z konta numer {result[4]}? (y/n)")
            if odp == "y":
                database_bank.wyplata_db_user(haslo_check,user_login,suma_wyplaty)
                database_bank.history_update(result,wyplata,oper,0)
            elif odp == "n":
                return
            else:
                print("Odpowiedzi niepoprawna. Sproboj raz jeszcze!")
                time.sleep(1)
            
        else:
            print("Bledne haslo do konta! Sproboj jeszcze raz..")
            time.sleep(1)
            return

    return
### |----------------------------------------|
def przelew_user_gielda(result, bilans_stan, bilans_gielda):
    oper = "Przelew z konta na gielde"
    prowizja_check = database_bank.prowizja_check()
    screen_clear()
    print("| Aktualny stan konta : ",round(bilans_stan, 2)," PLN")
    print("| Aktualny stan gieldy : ",round(bilans_gielda, 2)," PLN")
    wp_gielda = (input("| Jaka kwote chcesz przelac na gielde: "))
    try:
        wp_gielda = float(wp_gielda)
    except ValueError:
        print("Blednie podane dane...")
        time.sleep(1)
        return
    
    prowizja = wp_gielda * (prowizja_check[0] / 100)
    print("\n| Za przelew na gielde zostanie pobrana prowizja",prowizja_check[0],"%")
    print("| W tym przypadku wyniesie to : ",round(prowizja, 2)," PLN\n")
    odp = input("| Czy potwierdzasz ze chcesz dokonac przelewu z wyzej wymieniona prowizja? (y/n)")
    
    #wp_gielda += prowizja
    
    if odp == "n":
        print("Przerwano operacje ! Powrot do menu ! ...")
        time.sleep(2)
        return
    elif odp == "y":
        if wp_gielda > bilans_stan:
            #print("Razem: ",wp_gielda)
            print(f"| Podana kwota jest wieksza niz twoje aktualne saldo [{bilans_stan}], sproboj raz jeszcze!")
            print("| Potwierdz aby przejsc dalej!")
            getch()
        else:
            haslo_check = getpass("\n| Wprowadz haslo do konta: ")
            user_login = result[0]

            if haslo_check == result[1]:
                odp = input(f"| Czy potwierdzasz przelew kwoty {wp_gielda} na gielde z konta numer {result[4]}? (y/n)")
                if odp == "y":
                    bilans_stan =  bilans_stan - wp_gielda - prowizja
                    bilans_gielda = bilans_gielda + wp_gielda
                    database_bank.wp_user_gielda(haslo_check,user_login,bilans_stan, bilans_gielda)
                    database_bank.history_update(result,wp_gielda,oper,prowizja)
                    database_bank.bank_zarobek(prowizja)
                elif odp == "n":
                    return
                else:
                    print("Odpowiedzi niepoprawna. Sproboj raz jeszcze!")
                    time.sleep(1)
                
            else:
                print("Bledne haslo do konta! Sproboj jeszcze raz..")
                time.sleep(1)
                return
    else:
        print("Przerwano operacje ! Powrot do menu ! ...")
        time.sleep(2)
        return

    
    return
### |----------------------------------------|
def przelew_gielda_user(result, bilans_stan, bilans_gielda):
    oper = "Przelew z gieldy na konto"
    screen_clear()
    prowizja_check = database_bank.prowizja_check()
    print("| Aktualny stan konta : ",round(bilans_stan, 2)," PLN")
    print("| Aktualny stan gieldy : ",round(bilans_gielda, 2)," PLN")
    wy_gielda = (input("| Jaka kwote chcesz przelac z gieldy na konto: "))
    try:
        wy_gielda = float(wy_gielda)
    except ValueError:
        print("Blednie podane dane...")
        time.sleep(1)
        return
    
    prowizja = wy_gielda * (prowizja_check[1] / 100)
    print("\n| Za przelew na gielde zostanie pobrana prowizja",prowizja_check[1],"%")
    print("| W tym przypadku wyniesie to : ",prowizja,"\n")
    odp = input("| Czy potwierdzasz ze chcesz dokonac przelewu z wyzej wymieniona prowizja? (y/n)")
    
    if odp == "n":
        print("Przerwano operacje ! Powrot do menu ! ...")
        time.sleep(2)
        return
    elif odp == "y":
        if wy_gielda >= bilans_gielda:
            print(f"| Podana kwota jest wieksza niz twoje aktualne saldo na gieldzie [{bilans_gielda}], sproboj raz jeszcze!")
            print("| Potwierdz aby przejsc dalej!")
            getch()
        else:
        
            haslo_check = getpass("| Wprowadz haslo do konta: ")
            user_login = result[0]
        
            if haslo_check == result[1]:
                odp = input(f"| Czy potwierdzasz wyplate kwoty {wy_gielda} z gieldy na numer konta {result[4]}? (y/n)")
                if odp == "y":
                    bilans_stan = (bilans_stan + wy_gielda) - prowizja
                    bilans_gielda =  bilans_gielda - wy_gielda
                    database_bank.wy_gielda_user(haslo_check,user_login,bilans_stan, bilans_gielda)
                    database_bank.history_update(result,wy_gielda,oper,prowizja)
                    database_bank.bank_zarobek(prowizja)
                elif odp == "n":
                    return
                else:
                    print("Odpowiedzi niepoprawna. Sproboj raz jeszcze!")
                    time.sleep(1)
                
            else:
                print("Bledne haslo do konta! Sproboj jeszcze raz..")
                time.sleep(1)
                return
    else:
        print("Przerwano operacje ! Powrot do menu ! ...")
        time.sleep(2)
        return
 
    return
### |----------------------------------------|
def create_konto(result):
    oper = "Zakladanie konta klienta"
    screen_clear()
    password="1111"
 
    print("---------------------------------------------------")
    print("|                                                 |")
    print("| Tworzenie nowego konta :                  (***) |")
    print("|                                                 |")
    print("---------------------------------------------------")
    print("| Witaj ",result[2],result[3])
    print("|")
    while True:
        function_k = input("| Jaki rodzaj konta chcesz zalozyc (Klient(u) / Bankier(b) :")

        if function_k == "u":
            wynik = database_bank.check_account_number(function_k)[0]+1
        elif function_k == "b":
            wynik = database_bank.check_account_number(function_k)[0]+1
        else:
            print("bledny wybor")
            return
        print("| Numer konta klienta to :", wynik)
        name_K = input("| Podaj Imie klienta : ")
        surname_K = input("| Podaj Nazwisko klienta : ")
        login_K = input("| Podaj login do logowania klienta : ")
        now = datetime.datetime.now()
        current_time = now.strftime("%d-%m-%Y %H:%M:%S")
                
        print("|")
        print("| Wszystkie dane zostay podane sprawdz ich poprawnosc !")
        print("|")
        print("| Dane nowego konta : ")
        print("---------------------------------------------------\n")   
        print("| Imie i Nazwisko : ",name_K, surname_K)
        print("| Login konta : ",login_K)
        print("| Numer konta : ",wynik)
        if function_k == "u": 
            function = "Klient"
        else: function = "Bankier"
        print("| Funkcja konta : ", function)
        print("| Tymczasowe haslo (do zmiany podczas pierwszego ogowania): ",password)
        print("| Data utworzenie konta : ", current_time)
        print("---------------------------------------------------\n")
        wybor = input("| Czy potwierdzasz prawdziwosc danych i chcesz zalozyc takie konto? (y/n): ")

        if wybor == "y":
            database_bank.create_k(login_K,password,name_K,surname_K,wynik,function_k,current_time)
            database_bank.history_update(result,0,oper,0)
        elif wybor =="n":
            return
        else: 
            print("Bledny wybor, proces zostal przerwany ze wzgledu bezpiecznstwa")
            time.sleep(1)
            
        return
### |----------------------------------------|
def update_konto(result):
    oper = "Update konta klienta"
    screen_clear()
 
    print("------------------------------------------------------------------")
    print("|                                                                |")
    print("| Update informacji o koncie klienta :                     (***) |")
    print("|                                                                |")
    print("------------------------------------------------------------------")
    print("| Witaj ",result[2],result[3])
    print("|")
    numerk = input("| Podaj numer konta klienta ktore chcesz zobaczyc : ")

    try:
        float(numerk)
    except ValueError:
        print("Podana wartosc to nie cyfra. Ze wzgledow bezpieczenstwa nalezy powtorzyc operacje!")
        time.sleep(2)
        return

    odczyt_up = database_bank.odczyt_account(numerk)
    
    if not odczyt_up:
        print("Brak takiego numeru w bazie. Ze wzgledow bezpieczenstwa powtorz proces raz jeszcze!")
        time.sleep(2)
        return 
    else:
        screen_clear()
    
        print("------------------------------------------------------------------")
        print("|                                                                |")
        print("| Popraw dane klienta :                                    (***) |")
        print("|                                                                |")
        print("------------------------------------------------------------------")
        od_l = input(f"| Login -> ({odczyt_up[1]}) : ")
        if not od_l:
            od_l = odczyt_up[1]
        od_p = input(f"| Czy zresetowac haslo (y - for default reset - '1111') : ")
        if od_p == "y":
            od_p = "1111"
        elif not od_p:     
            od_p = odczyt_up[6]
        od_n = input(f"| Imie -> ({odczyt_up[2]}) : ")
        if not od_n:
            od_n = odczyt_up[2]
        od_s = input(f"| Nazwisko -> ({odczyt_up[3]}) : ")
        if not od_s:
            od_s = odczyt_up[3]
        print(f"| Numer konta -> ({odczyt_up[0]}) : ")
        print("------------------------------------------------------------------")
        print("| Sprawdz poprawnosc danych do aktualizacji : ")
        print("------------------------------------------------------------------")
        print("|")        
        print("| Login \t: ",od_l)
        if od_p == "1111": 
            print("| Haslo \t: > zresetowane")
        elif not od_p:
            print("| Haslo \t: ****** - bez zmiany")
        else:
            print("| Haslo \t: ****** - zmienione")
        print("| Imie \t\t: ",od_n)
        print("| Nazwisko \t: ",od_s)                
        print("|")
        print("| Numer konta : ",odczyt_up[0])
        print("|")        
        print("------------------------------------------------------------------")
        od_k = odczyt_up[0]
        potwierdz = input("| Czy potwierdzasz zmiane danych? (y/n) : ")
        if potwierdz == "y":
            database_bank.update_dancyh_klienta(od_l,od_p,od_n,od_s,od_k)
            database_bank.history_update(result,0,oper,0)
            return
        elif potwierdz == "n":
            return
        else:
            return
### |----------------------------------------|
def delete_konto(result):
    oper = "Usuniecie konta klienta"
    screen_clear()
 
    print("------------------------------------------------------------------")
    print("|                                                                |")
    print("| Usuwanie konta :                                         (***) |")
    print("|                                                                |")
    print("------------------------------------------------------------------")
    print("| Witaj ",result[2],result[3])
    print("|")
    database_bank.bilans_account()

    print("|")
    odp = input("| Czy chcesz skasowac ktores konto? (yes/no) : ")
    if odp == "yes":
        delnumber = input("| Ktore konto chcesz skasowac? Podaj numer konta (n = anuluj : ")

        try:
            float(delnumber)
        except ValueError:
            print("Blednie podane dane lub anulowano operacje...")
            time.sleep(1)
            return
        database_bank.list_delnumber_account(delnumber)
        database_bank.history_update(result,0,oper,0)
    elif odp == "no":
        return
    else:
        print("Bledna odpowiedz. Ze wzgledow bezpieczenstwa sproboj raz jeszcze!")
        time.sleep(2)
        return

    return
### |----------------------------------------|
def bilans_kont(result):  ### Bilans wszystkich kont
    oper = "Bilans wszystkich kont"
    screen_clear()
 
    print("---------------------------------------------------------------------------------------")
    print("|                                                                                     |")
    print("| Bilans wszystkich kont :                                                      (***) |")
    print("|                                                                                     |")
    print("---------------------------------------------------------------------------------------")
    print("| Witaj ",result[2],result[3])
    print("|")
    database_bank.bilans_account()
    database_bank.history_update(result,0,oper,0)
    print("|")
    print("---------------------------------------------------------------------------------------")
    print("| Aby przejsc dalej wcisnji dowolny przycisk...")
    getch()

    return
### |----------------------------------------|
def info_konto(result): ### 6. Wyciag z konta klienta
    oper = "Wyciag z konta klienta"
    
    screen_clear()
 
    print("------------------------------------------------------------------")
    print("|                                                                |")
    print("| Wyciag z konta klienta :                                 (***) |")
    print("|                                                                |")
    print("------------------------------------------------------------------")
    print("| Witaj ",result[2],result[3])
    print("|")
    numerk = input("| Podaj numer konta klienta ktore wyciag chcesz zobaczyc : ")

    try:
        float(numerk)
    except ValueError:
        print("Podana wartosc to nie cyfra. Ze wzgledow bezpieczenstwa nalezy powtorzyc operacje!")
        time.sleep(2)
        return

    odczyt = database_bank.odczyt_account(numerk)
    database_bank.history_update(result,0,oper,0)
    
    if not odczyt:
        print("Brak takiego numeru w bazie. Ze wzgledow bezpieczenstwa powtorz proces raz jeszcze!")
        time.sleep(2)
        return 
    else:
        screen_clear()

        print("------------------------------------------------------------------")
        print("| Wyciag z konta klienta :                                 (***) |")
        print("------------------------------------------------------------------")
        print("|")
        print("| Klient : \t\t",odczyt[2],odczyt[3])
        print("| Login : \t\t",odczyt[1])
        print("| Numer konta : \t",odczyt[0])
        print("|")
        print("| Saldo konta klienta : \t",round(odczyt[4], 2)," PLN")
        print("| Saldo konta gieldowego : \t",round(odczyt[5], 2)," PLN")
        print("|")
        print("| Data utworzenia konta : \t",odczyt[7])
        print("------------------------------------------------------------------")
        print("| Aby przejsc dalej wcisnji dowolny przycisk...")
        getch()
    return
### |----------------------------------------|
def historia_konta(result): ### 7. Historia aktywnosci / w banku i na koncie klienta
    oper = "Przegladanie historii aktywnosci klienta"
    screen_clear()
 
    print("------------------------------------------------------------------")
    print("|                                                                |")
    print("| Historia aktywnosci klienta : (aktywnosc/transakcje)     (***) |")
    print("|                                                                |")
    print("------------------------------------------------------------------")
    print("| Witaj ",result[2],result[3])
    print("|")
    numerk = input("| Podaj numer konta klienta ktore wyciag chcesz zobaczyc : ")

    try:
        float(numerk)
    except ValueError:
        print("Podana wartosc to nie cyfra. Ze wzgledow bezpieczenstwa nalezy powtorzyc operacje!")
        time.sleep(2)
        return

    odczyt = database_bank.odczyt_account(numerk)
    database_bank.history_update(result,0,oper,0)
    
    if not odczyt:
        print("Brak takiego numeru w bazie. Ze wzgledow bezpieczenstwa powtorz proces raz jeszcze!")
        time.sleep(2)
        return 
    else:
        screen_clear()
        print("--------------------------------------------------------------------------------------")
        print("| Historia aktywnosci klienta :   (aktywnosc bank / historia transakcji)       (***) |")
        print("--------------------------------------------------------------------------------------\n")
        wybor = input("| Co chcesz sprawdzic? (aktywnosc konta - [a] / historia transakcji - [t]) ? : ")
        
        if not wybor:
            print("Wybrano niepoprawna opcje. We wzgledu bezpieczenstwa powtorz operacje!")
            time.sleep(2)
            return
            
        elif wybor == "a" or "t":
            if wybor == "a":
                decyzja = "aktywnosc klienta"
            else: 
                decyzja = "historia transakcji"
            print("--------------------------------------------------------------------------------------")
            print("| Historia aktywnosci klienta :   (",decyzja,")")
            print("--------------------------------------------------------------------------------------\n")
            ile = input("| Ile ostatnich operacji chcesz zobaczy? Podaj liczbe : ")
            if not ile:
                ile = 99999
            database_bank.historia_konta(numerk,wybor,ile)
            dlugosc = database_bank.ilosc_rekordow(numerk,wybor)
            print("\n\n| W bazie znajdowalo sie tylko ",dlugosc, " rekordow.")
            print("| Aby przejsc dalej wcisnji \"Enter\" ...")
            getch()
            return
### |----------------------------------------|
def aktualnie_zalogowani(result): ### 8. Lista aktualnie zalogowanych uzytkownikow
    oper = "Lista zalogowanych klientow"
    screen_clear()
 
    print("---------------------------------------------------------------------------------------")
    print("|                                                                                     |")
    print("| Lista obecnie zalogowanych klientow :                                         (***) |")
    print("|                                                                                     |")
    print("---------------------------------------------------------------------------------------")
    print("|")
    database_bank.log_status_check()
    database_bank.history_update(result,0,oper,0)
    print("|")
    print("---------------------------------------------------------------------------------------")
    print("| Aby przejsc dalej wcisnji dowolny przycisk...")
    getch()

    return
### |----------------------------------------|
def zmiana_h(result):
    screen_clear()
    
    phas = getpass("| Podaj dotychczasowe haslo do Twojego konta : ")
    
    if phas == result[1]:
        has = getpass("| Podaj nowe haslo do Twojego konta : ")
        
        if has == "":
            screen_clear()
            print("Haslo nie moze byc puste!!! Rozpocznij proces raz jeszcz!")
            time.sleep(1)
            has = result[1]
            return has
        else:
            database_bank.has_update(result[0],result[1],has)
            print("Haslo zmienione mozesz zalogowac sie z nowym haslem!")
            time.sleep(1)            
            return has
    else:
        print("Podane dotychczasowe haslo jest niepoprawne, sproboj raz jeszcze !")
        time.sleep(2)
        has = result[1]
        return has
### |----------------------------------------|
def menu_bank():

    path_to_file = 'bank.db'
    path = Path(path_to_file)

    if path.is_file():    
      
        while True:
            
            screen_clear()
            
            print(f"{kolor.WARNING}---------------------------------------")
            print("| MICRO BANK - Witamy w naszym banku! |")
            print(f"---------------------------------------{kolor.ENDC}")

            menu = [
                "Logowanie",
                "Wylogowanie"
            ]

            for n in range(len(menu)):
                print(" {}.  {}".format(n+1, menu[n]))

            choice = input("\n #: ")

            if choice == "1":
                result = logowanie()
            elif choice == "2":
                # status = False
                # id = int(result[4])

                # database_bank.log_status_update(id,status)
                screen_clear()    
                break
            else:
                print("Nie ma takiej pozycji w menu, wybierz inna!")
                time.sleep(1)

    else:
        print(f'Plik bazy danych {path_to_file} nie istnieje. \nSkontaktuj sie z administratorem.')
        time.sleep(3)
        exit()



    sys.exit()
    #return
### |----------------------------------------|
def zmiana_oprocentowania(result):
    screen_clear()
    oper = "Zmiana oprocentowania dla wplat/wyplat na gielde"
    prowizja_check = database_bank.prowizja_check()
    
    print("------------------------------------------------------------------")
    print("|                                                                |")
    print("| Zmiana oprocenowania dla wplat/wyplat z gieldy :         (***) |")
    print("|                                                                |")
    print("------------------------------------------------------------------")
    print("| Witaj ",result[2],result[3])
    print("|")
    print("------------------------------------------------------------------")
    print("| Aktualna oprocentowanie wynosi :")
    print("| - dla wplat na gielde : ",prowizja_check[0], " %")
    print("| - dla wyplat z gieldy : ",prowizja_check[1], " %")
    print("------------------------------------------------------------------\n\n")
    
    pytanie = input("| Czy chcesz dokonac zmiany oprocentowania? (yes/no) :")

    if not pytanie:
        print("\nNiepoprawna odpowiedz. Ze wzgledu bezpieczenstwa powtorz operacje!")
        time.sleep(2)
        return
    elif pytanie == "yes":
        screen_clear()
        print("------------------------------------------------------------------")
        print("| Podaj nowe oprocentowanie. W przypadku braku zmian wcisnji \"Enter\":\n")
        new_prow_wp_gielda = input("| - Prowizja dla wplat na gielde : ")
        new_prow_wy_gielda = input("| - Prowizja wyplat z gieldy : ")
        if not new_prow_wp_gielda:
            new_prow_wp_gielda = prowizja_check[0]
        if not new_prow_wy_gielda:
            new_prow_wy_gielda = prowizja_check[1]
        print("------------------------------------------------------------------\n\n")

        try:
            float(new_prow_wp_gielda)
            float(new_prow_wy_gielda)
        except ValueError:
            print("Podana wartosc to nie cyfra lub nie wprowadziles zadnej wartosci. Ze wzgledow bezpieczenstwa nalezy powtorzyc operacje!")
            time.sleep(2)
            return

        # if not new_prow_wp_gielda:
        #     print("Nie zmieniono prowizji dla wplat na gielde!")
        # else:
        #     prow_wp_gielda = new_prow_wp_gielda

        # if not new_prow_wy_gielda:
        #     print("Nie zmieniono prowizji dla wyplat na gielde!")
        # else:
        #     prow_wy_gielda = new_prow_wy_gielda

        database_bank.prowizja_update(new_prow_wp_gielda,new_prow_wy_gielda)
        database_bank.history_update(result,0,oper,0)
            
    elif pytanie == "no":
        print("\nZadna zmiana nie zostala dokonana.")
        time.sleep(2)
        return

    


    return
### |----------------------------------------|
### |----------------------------------------|
### |----------------------------------------|
### |----------------------------------------|
### |----------------------------------------|

menu_bank()

### |----------------------------------------|

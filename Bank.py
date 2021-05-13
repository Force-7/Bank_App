from os import stat_result
import sqlite3
from prettytable import from_db_cursor


_Tabela = "Base"
connection = sqlite3.connect("Base.db")
cursor = connection.cursor()



# Tworzenie Tabeli
def create_table():  
    try:
        query = """CREATE TABLE IF NOT EXISTS main (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL, 
        password TEXT NOT NULL, 
        pomoc_pyt TEXT NOT NULL, 
        pomoc_odp TEXT NOT NULL, 
        balance INTEGER DEFAULT 0,
        euro INTEGER DEFAULT 0,
        dolar INTEGER DEFAULT 0,
        funt INTEGER DEFAULT 0,
        dostep TEXT DEFAULT "user")
        """
        cursor.execute(query)
        connection.commit()
        return True
    except:
        return False

# Dodawanie użytkownika
def check_user(username, password):

    query = f"SELECT username, password FROM main"
    result = cursor.execute(query).fetchall()


    for row in result:
        if username == row[0] and password == row[1]:
            return True
    return False

# Panel Administratora
def dostep(username):
    query = f"SELECT username, dostep FROM main"
    result = cursor.execute(query).fetchall()

    for row in result:
        permiss = "admin"
        if username == row[0] and permiss == row[1]:
            return True

    return False

def dostep_admin(username):
    dostep = str(input("Dostep: \n")).lower()
    cursor.execute(f"UPDATE main SET dostep = '{dostep}' WHERE username = '{username}'")
    connection.commit()

# Fukcje do Admina
def show_db():
    cursor.execute("SELECT * FROM main")
    table = from_db_cursor(cursor)

    return table

def delete_username():
    kto = int(input("Jakie ID chcesz usunać ?\n "))
    cursor.execute(f"DELETE FROM main WHERE ID = {kto}")
    print("Pomyślnie usunięto użytkownika")
    connection.commit()

def change_permission():
    
    komu = str(input("Podaj nazwę użytkownika, któremu chcesz nadać prawa: \n"))
    permission = str(input("Jakie prawa chcesz nadać (User, Admin) \n")).lower()
    
    czy_istnieje = check_username(komu)

    if czy_istnieje:
            
        cursor.execute(f"UPDATE main SET dostep = '{permission}' WHERE username = '{komu}'")
        connection.commit()
        print(f"Pomyślnie zmieniono prawa dostępu na ({permission})\n")
            
        


    else: 
        print("Nie masz wystarczających środków na koncie")
        print("Niepoprawny Username ")
        print("Spróbuj ponownie!") 

###############################################
def waluta():
    waluty = { 
    "euro" : 4.56, 
    "funt" : 5.28,
    "dolar" : 3.75,
    }
    return waluty

# Logowanie
def login(): 
    choice = 1
    if choice == 1:
        username = input("Username: ")
        password = input("Password: ")

            
            
        if check_user(username,password) == True:
            print("")
            print("Logowanie!")
            print(f"Hello, {username}")
            print("")
            return username
               
        elif check_user(username, password) == False:
            print("")
            print("Niepoprawny Username lub Password.")
            print("Spróbuj ponownie!") 
            print("")
            quit()

# Change Password
def change_password(username):
    choice = 4
    if choice == 4:
        print("")
        password = input("Podaj stare hasło: ")
        print("")
        if check_user(username,password) == True:
            password = input("Podaj nowe hasło: ")
            cursor.execute(f"UPDATE main SET password = '{password}' WHERE username = '{username}'")
            connection.commit()
            print("")
            print("Zmieniono hasło!")
            print("")
               
        elif check_user(username, password) == False:
            print("")
            print("Błędne hasło")
            print("Spróbuj ponownie!") 
            print("")
            quit()

# Sprawdza pomocnicze pytanie
def check_help(pomoc_pyt, pomoc_odp):

    query = f"SELECT pomoc_pyt, pomoc_odp, password, username FROM main"
    result = cursor.execute(query).fetchall()


    for row in result:
        if pomoc_pyt == row[0] and pomoc_odp == row[1]:
            return True, row[0], row[2], row[3] 
    return False, 0, 0, 0

# Pokazuje pomocnicze pytanie
def show_pomoc_pyt(username):
    result = cursor.execute(f"SELECT pomoc_pyt FROM main WHERE username = '{username}'").fetchall()
    
    for row in result:
        return row[0]

# Sprawdza username
def check_username(username):

    query = f"SELECT username FROM main"
    result = cursor.execute(query).fetchall()

    for row in result:
        if username == row[0]:
            return True
    return False

#Przypomnienie hasła
def przypomnienie_hasla(pomoc_pyt, username):
    choice = 3
    if choice == 3:
        print("")
        
        if check_username(username) == True:
            print(f"{pomoc_pyt}")
            pomoc_odp = input("Podaj Odpowiedz: ")
            check, pytanie, haslo, username = check_help(pomoc_pyt, pomoc_odp)
            if check == True:
                print(f"Twoje hasło to: {haslo} ")
            elif check == False:
                print("ERROR")
        elif check_username(username) == False:
            print("nie git")

# Pokazuje pomocnicze pytanie (password)
def show_pomoc_pyt_password(password):
    result = cursor.execute(f"SELECT pomoc_pyt FROM main WHERE password = '{password}'").fetchall()
    
    for row in result:
        return row[0]

# Sprawdza password 
def check_password(password):
    query = f"SELECT password FROM main"
    result = cursor.execute(query).fetchall()

    for row in result:
        if password == row[0]:
            return True
    return False

# Przypomnienie nazwy uztkownika
def przypomnienie_username(pomoc_pyt, password):
    choice = 4
    if choice == 4: 

        if check_password(password) == True:
            print(f"{pomoc_pyt}")
            pomoc_odp = input("Podaj odpowiedz: ")
            check, pytanie, haslo, username = check_help(pomoc_pyt,pomoc_odp)
            if check == True:
                print(f"Twoje username to: {username}")
            elif check == False:
                print("ERROR")
        elif check_password(password) == False:
            print("Błąd")

# Rejestracja
def registration():
    try:
        username = input("Give Username: ")
        password = input("Give Password: ")
        pomoc_pyt = input("Dodaj pomocnicze pytanie(Informacja potrzebna do odzyskania nazwy/hasła): ")
        pomoc_odp = input("Odpowiedz(Informacja potrzebna do odzyskania nazwy/hasła): ")
        cursor.execute(f"INSERT INTO main (username, password, pomoc_pyt, pomoc_odp) VALUES ( '{username}', '{password}', '{pomoc_pyt}', '{pomoc_odp}')")
        connection.commit()
        print("")
        print("Pomyślnie stworzono konto")
        print("")
    except:
        print("Nie udało się stworzyć konta!")
        print("Nazwa użytkownika zajeta") 

# Stan konta
def show_balance(username): 
    result = cursor.execute(f"SELECT balance FROM main WHERE username = '{username}'").fetchall()
    
    for row in result:
        return row[0]

# Wpłata
def add_balance(podane, username):
    try: 
        balance = input("Jaką kwotę chcesz wpłacić(PLN): ")
        if balance == "0":
            print("Powrót do Menu")
            return True
        else: 
            balance = int(balance) 
            if balance > 0:
                balance = podane + balance
                cursor.execute(f"UPDATE main SET balance = {balance} WHERE username = '{username}'")
                connection.commit()
                print("Pomyślnie dodano!")
            else: 
                print("Kwota musi być dodatnia!")
    except:
        return False

# Stan konta
def show_balance_euro(username): 
    result = cursor.execute(f"SELECT euro FROM main WHERE username = '{username}'").fetchall()
    
    for row in result:
        return row[0]

def show_balance_dolar(username): 
    result = cursor.execute(f"SELECT dolar FROM main WHERE username = '{username}'").fetchall()
    
    for row in result:
        return row[0]

def show_balance_funt(username): 
    result = cursor.execute(f"SELECT funt FROM main WHERE username = '{username}'").fetchall()
    
    for row in result:
        return row[0]


# # Dodawanie Euro
# def add_waluty(podane, username):
#     try: 
#         balance_waluty = input("Jaką kwotę chcesz wpłacić(EURO): ")
#         if balance_euro == "0":
#             print("Powrót do Menu")
#             return True
#         else: 
#             balance_euro = int(balance_euro) 
#             if balance_euro > 0:
#                 balance_euro = podane + balance_euro
#                 cursor.execute(f"UPDATE main SET euro = {balance_euro} WHERE username = '{username}'")
#                 connection.commit()
#                 print(f"Pomyślnie dodano, twój obecny stan konta: {balance_euro} !")
#             else: 
#                 print("Kwota musi być dodatnia!")
#     except:
#         return False

# Zmiana waluty 
def change_currency(podane_pln, username, nazwa_waluty):
    
    try:
        balance_1 = input("Ile chcesz wymienić(PLN)\n")
        nazwa_waluta = str(input("Jaką walutę chcesz otrzymać?\n")).lower()

        if balance_1 == 0:
            print("Powrót do Menu")
            return True
        else:
            balance_1 = int(balance_1)
            if balance_1 >= 1 and nazwa_waluta == "euro":
                odejmowanie_kwoty = podane_pln - balance_1
                suma = show_balance_euro(username)
                dodawanie_walut = suma + balance_1 / nazwa_waluty[nazwa_waluta]
                dodawanie_walut = "{:.2f}".format(dodawanie_walut)
                
                if podane_pln >= balance_1:
                    cursor.execute(f"UPDATE main SET euro = {dodawanie_walut} WHERE username = '{username}'")
                    cursor.execute(f"UPDATE main SET balance = {odejmowanie_kwoty} WHERE username = '{username}'")
                    connection.commit()
                    print(f"Pomyślnie przewalutowano podaną kwotę {balance_1}PLN na {dodawanie_walut} Euro")
                else:
                    print("Nie masz wystarczająco środków")

            elif balance_1 >= 1 and nazwa_waluta == "dolar":
                odejmowanie_kwoty = podane_pln - balance_1
                suma = show_balance_dolar(username)
                dodawanie_walut = suma + balance_1 / nazwa_waluty[nazwa_waluta]
                dodawanie_walut = "{:.2f}".format(dodawanie_walut)

                if podane_pln >= balance_1:
                    cursor.execute(f"UPDATE main SET dolar = {dodawanie_walut} WHERE username = '{username}'")
                    cursor.execute(f"UPDATE main SET balance = {odejmowanie_kwoty} WHERE username = '{username}'")
                    connection.commit()
                    print(f"Pomyślnie przewalutowano podaną kwotę {balance_1}PLN na {dodawanie_walut} Dolarów")
                else:
                    print("Nie masz wystarczająco środków")

            elif balance_1 >= 1 and nazwa_waluta == "funt":
                odejmowanie_kwoty = podane_pln - balance_1
                suma = show_balance_funt(username)
                dodawanie_walut = suma + balance_1 / nazwa_waluty[nazwa_waluta] 
                dodawanie_walut = "{:.2f}".format(dodawanie_walut)

                if podane_pln >= balance_1:
                    cursor.execute(f"UPDATE main SET funt = {dodawanie_walut} WHERE username = '{username}'")
                    cursor.execute(f"UPDATE main SET balance = {odejmowanie_kwoty} WHERE username = '{username}'")
                    connection.commit()
                    print(f"Pomyślnie przewalutowano podaną kwotę {balance_1}PLN na {dodawanie_walut} Funtów")
                else:
                    print("Nie masz wystarczająco środków")

            else:
                print("Nie masz wystarczających środków")

    except:
        return False

# Wypłata
def withdraw(podane, username):
    
    try: 
        balance = input("Jaką kwotę chcesz wypłacić: ")
        if balance == "0":
            print("Powrót do Menu")
            return True
        else: 
            balance = int(balance)

            if balance <= podane and balance > 0:
                balance = podane - balance
                cursor.execute(f"UPDATE main SET balance = {balance} WHERE username = '{username}'")
                connection.commit()
                print("Podana kwota została wypłacona!")

            else:
                print("Nie masz wystarczających środków")

    except:
        return False
######################################################
# Transfer
def transfer(username, podane_pln):
    try:
        do_kogo = str(input("Podaj nazwę użytkownika(Odbiorcy): \n"))
        kwota_przelewu = int(input("Jaka kwotę chcesz przelać: \n"))
        
        czy_istnieje = check_username(do_kogo)

        if kwota_przelewu <= podane_pln and czy_istnieje:
            przelew_wych = podane_pln - kwota_przelewu

            stan_odb = show_balance(do_kogo)
            przelew_odb = stan_odb + kwota_przelewu 
            cursor.execute(f"UPDATE main SET balance = {przelew_wych} WHERE username = '{username}'")
            cursor.execute(f"UPDATE main SET balance = {przelew_odb} WHERE username = '{do_kogo}'")
            connection.commit()
            print(f"Pomyślnie przelano kwotę ({kwota_przelewu}) PLN\n")
                
            


        else: 
            print("Nie masz wystarczających środków na koncie")
            print("Niepoprawny Username ")
            print("Spróbuj ponownie!") 
    except:
        return False

######################################################
# Main
def main():
    while True:
        create_table()
        print("##################################")
        print("#                                #")
        print("# 1. Zaloguj się                 #")
        print("# 2. Rejestracja                 #")
        print("# 3. Przypomnienie hasła/nazwy   #")
        print("# 4. Wyjdź                       #")
        print("#                                #")
        print("##################################")

        user_choice = int(input("Wybierz cyfrę: "))
        print("")
        
       
        if user_choice == 1:
            username = login()
            
            while True:
                

                print("############################")
                print("#  1. Wpłata pieniędzy     #")
                print("#  2. Wypłata pieniedzy    #")
                print("#  3. Stan konta           #")
                print("#  4. Zmiana hasła         #")
                print("#  5. Przewalutowanie      #")
                print("#  6. Przelew              #")
                print("#  7. Wyloguj              #")
                if dostep(username) == True:
                    print("#  9. Panel Administartora #") 
                print("############################")

                user_choice1 = int(input("Podaj Cyfrę: "))
                
                if user_choice1 == 9:
                    if dostep(username) == True:
                        
                        print("########################################")
                        print("#  1. Wyświetlanie DB                  #")
                        print("#  2. Usuwanie uzytkownika (ID)        #")
                        print("#  3. Zmiana praw dostępu              #")
                        print("########################################")   

                        user_choice2 = int(input("Podaj Cyfrę: "))

                        if user_choice2 == 1:
                            pokaz = show_db()
                            print(pokaz)
                           

                        if user_choice2 == 2:
                            delete_username()
                            
                        if user_choice2 == 3:
                            change_permission()

                if user_choice1 == 0: # NADAWANIE DOSTEPU 1-raz Input"admin"
                    dostep_admin(username)

                if user_choice1 == 1:                     
                    podane = show_balance(username)
                    add_balance(podane, username)
        


                if user_choice1 == 2:
                        podane = show_balance(username)
                        withdraw(podane, username)
                        

                if user_choice1 == 3:
                    balance = show_balance(username)
                    balance_euro = show_balance_euro(username)
                    balance_dolar = show_balance_dolar(username)
                    balance_funt = show_balance_funt(username)

                    print("##########################")
                    print("# Twój stan konta(PLN): ", balance)
                    print("# Twój stan konta(Euro): ", balance_euro)
                    print("# Twój stan konta(Dolar): ", balance_dolar)
                    print("# Twój stan konta(Funt): ", balance_funt)
                    print("##########################")

                if user_choice1 == 4:
                    password = change_password(username)

                if user_choice1 == 5:
                    nazwa_waluty = waluta()
                    podane_pln = show_balance(username)
                    change_currency(podane_pln, username, nazwa_waluty)

                if user_choice1 == 6:
                    podane_pln = show_balance(username)
                    transfer(username, podane_pln)

                if user_choice1 == 7:
                    print("")
                    print("Wylogowano!")
                    print("")
                    break

                

        if user_choice == 2:
            registration()


        if user_choice == 3:
            while True:
                print("##### Przypomnienie ########")
                print("#  1. Przypomnienie hasła  #")
                print("#  2. Przypomnienie nazwy  #")
                print("#  3. Back                 #")
                print("############################")
                
                user_choice2 = int(input("Podaj Cyfrę: "))

                if user_choice2 == 1:
                    username = input("Podaj Username: ")
                    pomoc_pyt = show_pomoc_pyt(username)
                    przypomnienie_hasla(pomoc_pyt, username)

                if user_choice2 == 2:
                    password = input("Podaj Hasło: ")
                    a = show_pomoc_pyt_password(password)
                    przypomnienie_username(a, password)


                if user_choice2 == 3:
                    break

        if user_choice == 4:
            print("Wyłączanie aplikacji")
            connection.close()
            break

if __name__ == '__main__':
    main()




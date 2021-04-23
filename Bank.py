import sqlite3


_Tabela = "Base"
connection = sqlite3.connect("Base.db")
cursor = connection.cursor()

# Zapisywanie nazyw uzytowniaka/ Zmienna, Podawac do funkcji do której jest porzebna(Show_balance)


# Tabela
def create_table():
    try:
        query = "CREATE TABLE IF NOT EXISTS main (username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, balance INTEGER DEFAULT 0) "
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



    
# Logowanie
def login(): 
    choice = 1
    if choice == 1:
        username = input("Nazwa: ")
        password = input("Hasło: ")

            
            
        if check_user(username,password) == True:
            print("")
            print("Logowanie!")
            print("")
            return username
               
        elif check_user(username, password) == False:
            print("")
            print("Spróbuj ponownie!") 
            print("")
            quit()
            


# Rejestracja
def registration():
    try:
        username = input("Podaj nazwę: ")
        password = input("Podaj hasło: ")
        cursor.execute(f"INSERT INTO main (username, password) VALUES ( '{username}', '{password}' )")
        connection.commit()
    except:
        print("Nie udało się stworzyć konta!")

# Stan konta
def show_balance(username): 
    result = cursor.execute(f"SELECT balance FROM main WHERE username = '{username}'").fetchall()
    
    for row in result:
        return row[0]



# Wpłata
def add_balance(podane, username):
    try: 
        balance = input("Jaką kwotę chcesz wpłacić: ")
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
                print("Pomyślnie dodano!")

            else:
                print("Nie masz wystarczających środków")

    except:
        return False

# Main
def main():
    while True:
        create_table()
        print("##########################")
        print("")
        print("1. Zaloguj się")
        print("2. Rejestracja")
        print("3. Wyjdź")
        print()
        print("##########################")

        user_choice = int(input("Wybierz cyfrę: "))
        print("")

        if user_choice == 1:
            username = login()
            
            while True:
                print("##########################")
                print("1. Wpłata pieniędzy")
                print("2. Wypłata pieniedzy")
                print("3. Stan konta")
                print("4. Wyloguj")
                print("##########################")

                user_choice1 = int(input("Podaj Cyfrę: "))

                if user_choice1 == 1:
                    
                    podane = show_balance(username)
                    add_balance(podane, username)
                    
                    
                if user_choice1 == 2:
                    podane = show_balance(username)
                    withdraw(podane, username)
                

                if user_choice1 == 3:
                    balance = show_balance(username)
                    print("###########################")
                    print("Twój stan konta: ", balance)
                    print("###########################")

                if user_choice1 == 4:
                    connection.close()
                    print("Wylogowano!")
                    return

        if user_choice == 2:
            registration()

        if user_choice == 3:
            print("Wyłączanie aplikacji")
            connection.close()
            break

if __name__ == '__main__':
    main()







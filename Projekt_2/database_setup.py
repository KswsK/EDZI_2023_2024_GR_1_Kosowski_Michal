import sqlite3

def create_tables():
    conn = sqlite3.connect('job_offers.db')
    cursor = conn.cursor()

    # Tworzenie tabeli Kategoria i wstawienie wartości na sztywno
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Kategoria (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nazwa TEXT
    )
    ''')

    cursor.execute('''
    INSERT INTO Kategoria (Nazwa) VALUES ('BigData/Data Science')
    ''')

    cursor.execute('''
    INSERT INTO Kategoria (Nazwa) VALUES ('Data')
    ''')

    # Tworzenie tabeli Źródło i wstawienie wartości na sztywno
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Zrodlo (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nazwa TEXT
    )
    ''')

    cursor.execute('''
    INSERT INTO Zrodlo (Nazwa) VALUES ('Justjoin.it')
    ''')

    # Tworzenie pozostałych tabel
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Firma (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nazwa TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Stanowisko (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nazwa TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Umiejetnosc (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nazwa TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Waluta (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Nazwa TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Oferta (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ID_Stanowiska INTEGER,
        ID_Firmy INTEGER,
        ID_Kategorii INTEGER,
        ID_Waluty INTEGER,
        ID_Zrodla INTEGER,
        Link TEXT,
        Umiejetnosci TEXT,
        Doswiadczenie TEXT,
        Wynagrodzenie_MIN REAL,
        Wynagrodzenie_MAX REAL,
        FOREIGN KEY (ID_Stanowiska) REFERENCES Stanowisko(ID),
        FOREIGN KEY (ID_Firmy) REFERENCES Firma(ID),
        FOREIGN KEY (ID_Kategorii) REFERENCES Kategoria(ID),
        FOREIGN KEY (ID_Waluty) REFERENCES Waluta(ID),
        FOREIGN KEY (ID_Zrodla) REFERENCES Zrodlo(ID)
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()

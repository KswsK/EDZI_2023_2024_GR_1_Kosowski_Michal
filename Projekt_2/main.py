from scrape_jobs import scrape_job_links_and_create_dataframe, scrape_job_titles
from database_setup import create_tables
import sqlite3
import json


def main():
    # Scrapowanie ofert pracy i tworzenie ramki danych
    url = "https://justjoin.it/krakow/data/experience-level_junior.mid.senior/with-salary_yes"
    df = scrape_job_links_and_create_dataframe(url)

    if df is not None:
        # Scrapowanie szczegółowych informacji o ofertach pracy
        job_titles, company_names, widelkis, walutas, umis, doss = scrape_job_titles(df)

        # Tworzenie lub czyszczenie tabel w bazie danych
        create_tables()

        # Zapisywanie szczegółowych informacji do bazy danych
        conn = sqlite3.connect('job_offers.db')
        cursor = conn.cursor()

        # Dodawanie unikalnych umiejętności do bazy danych
        for umiejetnosc_lista in umis:
            for umiejetnosc in umiejetnosc_lista:
                cursor.execute('SELECT ID FROM Umiejetnosc WHERE Nazwa = ?', (umiejetnosc,))
                umiejetnosc_id = cursor.fetchone()
                if not umiejetnosc_id:
                    cursor.execute('INSERT INTO Umiejetnosc (Nazwa) VALUES (?)', (umiejetnosc,))
                    umiejetnosc_id = cursor.lastrowid
                else:
                    umiejetnosc_id = umiejetnosc_id[0]

        # Przetwarzanie ofert pracy i dodawanie ich do bazy danych
        for i in range(len(df)):
            cursor.execute('SELECT ID FROM Firma WHERE Nazwa = ?', (company_names[i],))
            firma_id = cursor.fetchone()
            if not firma_id:
                cursor.execute('INSERT INTO Firma (Nazwa) VALUES (?)', (company_names[i],))
                firma_id = cursor.lastrowid
            else:
                firma_id = firma_id[0]

            cursor.execute('SELECT ID FROM Stanowisko WHERE Nazwa = ?', (job_titles[i],))
            stanowisko_id = cursor.fetchone()
            if not stanowisko_id:
                cursor.execute('INSERT INTO Stanowisko (Nazwa) VALUES (?)', (job_titles[i],))
                stanowisko_id = cursor.lastrowid
            else:
                stanowisko_id = stanowisko_id[0]

            # Pobieranie ID kategorii na podstawie nazwy stanowiska
            kategoria_id = None
            if "BigData" in job_titles[i] or "Big Data" in job_titles[i] or "Data Science" in job_titles[
                i] or "Data Engineer" in job_titles[i]:
                cursor.execute('SELECT ID FROM Kategoria WHERE Nazwa = ?', ("BigData/Data Science",))
                kategoria_id = cursor.fetchone()
            else:
                cursor.execute('SELECT ID FROM Kategoria WHERE Nazwa = ?', ("Data",))
                kategoria_id = cursor.fetchone()

            if not kategoria_id:
                kategoria_id = 0
            else:
                kategoria_id = kategoria_id[0]

            cursor.execute('SELECT ID FROM Waluta WHERE Nazwa = ?', (walutas[i],))
            waluta_id = cursor.fetchone()
            if not waluta_id:
                cursor.execute('INSERT INTO Waluta (Nazwa) VALUES (?)', (walutas[i],))
                waluta_id = cursor.lastrowid
            else:
                waluta_id = waluta_id[0]

            cursor.execute('SELECT ID FROM Zrodlo WHERE Nazwa = ?', ("Justjoin.it",))
            zrodlo_id = cursor.fetchone()
            if not zrodlo_id:
                cursor.execute('INSERT INTO Zrodlo (Nazwa) VALUES (?)', ("Justjoin.it",))
                zrodlo_id = cursor.lastrowid
            else:
                zrodlo_id = zrodlo_id[0]

            umiejetnosci_str = ', '.join(umis[i])
            doswiadczenie_str = ', '.join(doss[i])

            cursor.execute(
                'INSERT INTO Oferta (ID_Stanowiska, ID_Firmy, ID_Kategorii, ID_Waluty, ID_Zrodla, Link, Umiejetnosci, Doswiadczenie, Wynagrodzenie_MIN, Wynagrodzenie_MAX) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (stanowisko_id, firma_id, kategoria_id, waluta_id, zrodlo_id, 'justjoin.it' + df['Link do oferty'][i],
                 umiejetnosci_str, doswiadczenie_str, widelkis[i][0], widelkis[i][1]))

        conn.commit()
        conn.close()

        # Zapisywanie informacji o ofertach pracy do pliku JSON
        Oferty_JJ = df.copy()
        Oferty_JJ['Stanowisko'] = job_titles
        Oferty_JJ['Firma'] = company_names
        Oferty_JJ['Umiejętności'] = umis
        Oferty_JJ['Doświadczenie'] = doss
        Oferty_JJ['Waluta'] = walutas
        Oferty_JJ['Minimalne wynagrodzenie'] = [w[0] for w in widelkis]
        Oferty_JJ['Maksymalne wynagrodzenie'] = [w[1] for w in widelkis]
        #Oferty_JJ['Kategoria'] = Oferty_JJ['Stanowisko'].apply(kategoria)
        Oferty_JJ['Źródło'] = 'Justjoin.it'
        Oferty_JJ.rename(columns={'Link do oferty': 'Link'}, inplace=True)
        Oferty_JJ = Oferty_JJ.reindex(columns=['ID', 'Źródło', 'Link', 'Stanowisko', 'Firma', 'Minimalne wynagrodzenie',
                                               'Maksymalne wynagrodzenie', 'Waluta', 'Umiejętności', 'Kategoria', 'Doświadczenie'])
        Oferty_JJ.to_json('Oferty_JJ.json', orient='records')
    else:
        print("Brak danych do przetworzenia.")

if __name__ == "__main__":
    main()

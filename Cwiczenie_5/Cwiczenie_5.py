import pandas as pd
import requests

miasta = [
    "Katowice",
    "Krakow",
    "Rzeszow",
    "Opole",
    "Wroclaw",
    "Lodz",
    "Kielce",
    "Lublin",
    "Warszawa",
    "Gorzow",
    "Zielona Gora",
    "Poznan",
    "Torun",
    "Olsztyn",
    "Bialystok",
    "Gdansk",
    "Szczecin",
]

def pobierz_dane_stacji(nazwa_stacji):
    url = f"https://danepubliczne.imgw.pl/api/data/synop/station/{nazwa_stacji}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Wystąpił problem podczas pobierania danych dla stacji {nazwa_stacji}.")
        return None

def utworz_df(dane):
    df = pd.DataFrame([dane])
    return df[["id_stacji", "stacja", "data_pomiaru", "godzina_pomiaru", "temperatura", 
               "predkosc_wiatru", "kierunek_wiatru", "wilgotnosc_wzgledna", "suma_opadu", "cisnienie"]]

frames = []

for miasto in miasta:
    nazwa_stacji = miasto.replace(" ", "").lower()
    dane_json = pobierz_dane_stacji(nazwa_stacji)
    if dane_json:
        df = utworz_df(dane_json)
        frames.append(df)

pogoda_df = pd.concat(frames, ignore_index=True)

pogoda_df["temperatura"] = pogoda_df["temperatura"].astype(float)
pogoda_df["suma_opadu"] = pogoda_df["suma_opadu"].astype(float)
pogoda_df["cisnienie"] = pogoda_df["cisnienie"].astype(float)

# Średnia temperatura
srednia_temperatura = pogoda_df["temperatura"].mean()
print(f"Średnia temperatura: {srednia_temperatura:.2f} °C")

# Minimalna temperatura wraz ze stacją
min_temperatura = pogoda_df.loc[pogoda_df["temperatura"].idxmin()]
print(f"Minimalna temperatura: {min_temperatura['temperatura']} °C w stacji: {min_temperatura['stacja']}")

# Maksymalna temperatura wraz ze stacją
max_temperatura = pogoda_df.loc[pogoda_df["temperatura"].idxmax()]
print(f"Maksymalna temperatura: {max_temperatura['temperatura']} °C w stacji: {max_temperatura['stacja']}")

# Data i godzina pomiaru
data_i_godzina = pd.to_datetime(pogoda_df["data_pomiaru"] + " " + pogoda_df["godzina_pomiaru"], format="%Y-%m-%d %H").unique()
print(f"Data i godzina pomiaru: {data_i_godzina}")

# Średnia wartość opadów
srednia_opady = pogoda_df["suma_opadu"].mean()
print(f"Średnia wartość opadów: {srednia_opady:.2f} mm")

# Minimalna wartość opadów wraz ze stacją
min_opady = pogoda_df.loc[pogoda_df["suma_opadu"].idxmin()]
print(f"Minimalne opady: {min_opady['suma_opadu']} mm w stacji: {min_opady['stacja']}")

# Maksymalna wartość opadów wraz ze stacją
max_opady = pogoda_df.loc[pogoda_df["suma_opadu"].idxmax()]
print(f"Maksymalne opady: {max_opady['suma_opadu']} mm w stacji: {max_opady['stacja']}")

# Średnia wartość ciśnienia
srednie_cisnienie = pogoda_df["cisnienie"].mean()
print(f"Średnie ciśnienie: {srednie_cisnienie:.2f} hPa")

# Minimalna wartość ciśnienia wraz ze stacją
min_cisnienie = pogoda_df.loc[pogoda_df["cisnienie"].idxmin()]
print(f"Minimalne ciśnienie: {min_cisnienie['cisnienie']} hPa w stacji: {min_cisnienie['stacja']}")

# Maksymalna wartość ciśnienia wraz ze stacją
max_cisnienie = pogoda_df.loc[pogoda_df["cisnienie"].idxmax()]
print(f"Maksymalne ciśnienie: {max_cisnienie['cisnienie']} hPa w stacji: {max_cisnienie['stacja']}")

# Zapisanie ramki danych do pliku JSON
pogoda_df.to_json("Pogoda.json", orient="records")
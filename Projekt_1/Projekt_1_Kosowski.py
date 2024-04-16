import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from collections import defaultdict
import seaborn as sns
import matplotlib.pyplot as plt
import json

# Funkcja do pobierania linków do ofert pracy i tworzenia ramki danych
def scrape_job_links_and_create_dataframe(url):
    # Funkcja do pobierania zawartości strony
    def get_page_content(url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            print("Nie udało się pobrać zawartości strony.")
            return None
    
    page_content = get_page_content(url)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Inicjalizacja listy do przechowywania linków
        job_links = []
        
        # Scrapowanie linków
        offer_list = soup.find_all('div', class_='css-2crog7')
        for offer in offer_list:
            job_links.append(offer.find('a', class_='offer_list_offer_link')['href'])
        
        # Tworzenie ramki danych z linkami
        df = pd.DataFrame({'ID': range(1, len(job_links)+1), 'Link do oferty': job_links})
        return df
    else:
        return None

# Przykładowe użycie
url = "https://justjoin.it/krakow/data/experience-level_junior.mid.senior/with-salary_yes"
df = scrape_job_links_and_create_dataframe(url)

# Funkcja do pobierania zawartości strony
def get_page_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        print("Nie udało się pobrać zawartości strony.")
        return None
    
# Funkcja do scrapowania stanowiska, nazwy firmy i widełek z podanego linku
def scrape_job_title(url):
    page_content = get_page_content(url)
    if page_content:
        soup = BeautifulSoup(page_content, 'html.parser')
        
        # Scrapowanie stanowiska
        job_div = soup.find('div', class_='css-1hwyvm5')
        if job_div:
            job_title_element = job_div.find('h1')
            if job_title_element:
                job_title = job_title_element.text.strip()
            else:
                job_title = "Nie udało się znaleźć stanowiska"
        else:
            job_title = "Nie udało się znaleźć stanowiska"
        
        # Scrapowanie nazwy firmy
        firma_div = soup.find('div', class_="css-31phsu")
        if firma_div:
            company_name_element = firma_div.find('div', class_='css-mbkv7r')
            if company_name_element:
                company_name = company_name_element.text.strip()
            else:
                company_name = "Nie udało się znaleźć nazwy firmy"
        else:
            company_name = "Nie udało się znaleźć nazwy firmy"
        
        # Scrapowanie widełek
        widelki_div = soup.find('div', class_="css-1d9s327")
        if widelki_div:
            widelki_name_elements = widelki_div.find_all('span', class_="css-1pavfqb")
            widelki_t = []
            for element in widelki_name_elements:
                widelki_text = element.text.strip()
                numbers = re.findall(r'\d+', widelki_text)
                widelki_t.extend(numbers)
            # Złącz każde 2 sąsiadujące elementy z widelki_t
            merged_widelki = [int(widelki_t[i] + widelki_t[i+1]) for i in range(0, len(widelki_t), 2)]
            
            # Dodatkowy warunek: jeśli w span class="css-1waow8k" jest "Net/month - B2B", przemnóż pierwsze 2 liczby w merged_widelki przez 1.23
            net_month_element = widelki_div.find('span', class_="css-1waow8k")
            if net_month_element and "Net/month - B2B" in net_month_element.text:
                merged_widelki[0] *= 1.23
                merged_widelki[1] *= 1.23
                
                # Zaokrąglenie wyniku mnożenia przez 1.23 do dwóch miejsc po kropce
                merged_widelki[0] = round(merged_widelki[0], 2)
                merged_widelki[1] = round(merged_widelki[1], 2)
        else:
            merged_widelki = "Nie udało się znaleźć widełek"
        
        # Scrapowanie waluty
        waluta_div = soup.find('div', class_="css-1d9s327")
        if waluta_div:
            waluta_name_elements = waluta_div.find('span', class_="css-1pavfqb")
            if waluta_name_elements:
                waluta_name = waluta_name_elements.text.strip()[-3:]
            else:
                waluta_name = "Nie udało się znaleźć nazwy waluty"
        else:
            waluta_name = "Nie udało się znaleźć nazwy waluty"
        

        # Scrapowanie umiejętności
        umi_div = soup.find('div', class_="MuiBox-root css-e6hxrt")
        if umi_div:
            umi_name_elements = umi_div.find_all('h6', class_='MuiTypography-root MuiTypography-subtitle2 css-x1xnx3')
            umi_t = []
            for element in umi_name_elements:
                umi_text = element.text.strip()
                umi_t.append(umi_text)
        else:
            umi_t = "Nie udało się znaleźć umiejętności"
        
         # Scrapowanie doświadczenia
        dos_div = soup.find('div', class_="css-zhwmgm")
        if dos_div:
            dos_name_elements = dos_div.find_all('div', class_="css-15wyzmd")
            dos_t = []
            for element in dos_name_elements:
                dos_text = element.text.strip()
                dos_t.append(dos_text)
        else:
            dos_t = "Nie udało się znaleźć umiejętności"
        
        return job_title, company_name, merged_widelki, waluta_name, umi_t, dos_t
    
# Funkcja do iteracji po linkach w kolumnie 'Link' i scrapowania stanowiska, nazwy firmy oraz widełek
def scrape_job_titles(df):
    job_titles = []
    company_names = []
    widelkis = []
    walutas = []
    umis = []
    doss = []
    for link in df['Link do oferty']:
        job_title, company_name, widelki, waluta, umi, dos = scrape_job_title("https://justjoin.it"+link)
        job_titles.append(job_title)
        company_names.append(company_name)
        widelkis.append(widelki)
        walutas.append(waluta)
        umis.append(umi)
        doss.append(dos)
    return job_titles, company_names, widelkis, walutas, umis, doss

# Scrapowanie stanowisk, nazw firm i widełek
job_titles, company_names, widelkis, walutas, umis, doss = scrape_job_titles(df)

# Tworzenie nowego DataFrame z wynikami
Oferty_JJ = pd.DataFrame({'ID': df.index + 1, 'Stanowisko': job_titles, 'Firma': company_names, 'Widelki': widelkis, 'Waluta': walutas, 'Umiejętności': umis, 'Doświadczenie': doss})
# Sortowanie i wybieranie pierwszego i ostatniego elementu dla każdej listy
Oferty_JJ['Widelki'] = Oferty_JJ['Widelki'].apply(lambda x: [sorted(x)[0], sorted(x)[-1]] if isinstance(x, list) else x)
Oferty_JJ['Doświadczenie'] = Oferty_JJ['Doświadczenie'].apply(lambda x: x[1] if isinstance(x, list) else x)

def kategoria(stanowisko):
    if "BigData" in stanowisko or "Big Data" in stanowisko or "Data Science" in stanowisko or "Data Engineer" in stanowisko:
        return "BigData/Data Science"
    else:
        return "Data"
Oferty_JJ['Kategoria'] = Oferty_JJ['Stanowisko'].apply(kategoria)

Oferty_JJ['Źródło'] = 'Justjoin.it'
Oferty_JJ['Minimalne wynagrodzenie'] = Oferty_JJ['Widelki'].apply(lambda x: x[0] if isinstance(x, list) else None)
Oferty_JJ['Maksymalne wynagrodzenie'] = Oferty_JJ['Widelki'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None)

Oferty_JJ['Źródło'] = 'Justjoin.it'
Oferty_JJ['Minimalne wynagrodzenie'] = Oferty_JJ['Widelki'].apply(lambda x: x[0] if isinstance(x, list) else None)
Oferty_JJ['Maksymalne wynagrodzenie'] = Oferty_JJ['Widelki'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None)

Oferty_JJ.drop(columns=['Widelki'], inplace=True)

df['Link do oferty'] = "justjoin.it" + df['Link do oferty']
Oferty_JJ['Link'] = df['Link do oferty']

desired_columns_order = ['ID', 'Źródło', 'Link', 'Stanowisko', 'Firma', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie', 'Waluta', 'Umiejętności', 'Kategoria', 'Doświadczenie']
Oferty_JJ = Oferty_JJ.reindex(columns=desired_columns_order)

Oferty_JJ.to_json('Oferty_JJ.json', orient='records')

# Inicjalizacja słownika do przechowywania liczby wystąpień umiejętności
skills_count = defaultdict(int)

# Iteracja po każdym wierszu DataFrame
for skills_list in Oferty_JJ['Umiejętności']:
    # Iteracja po każdej umiejętności w liście umiejętności
    for skill_group in skills_list:
        # Dzielenie grupy umiejętności po znaku '/'
        skills = skill_group.split('/')
        # Iteracja po każdej umiejętności w grupie
        for skill in skills:
            # Usunięcie ewentualnych białych znaków na początku i końcu umiejętności
            skill = skill.strip()

            skills_count[skill] += 1

sorted_skills_count = dict(sorted(skills_count.items(), key=lambda item: item[1], reverse=True))

# Pobranie top 10 umiejętności
top_skills = list(sorted_skills_count.keys())[:10]
counts = [sorted_skills_count[skill] for skill in top_skills]

# Tworzenie wykresu
plt.figure(figsize=(10, 6))
plt.barh(top_skills, counts, color='skyblue')
plt.xlabel('Liczba wystąpień')
plt.ylabel('Umiejętność')
plt.title('Top 10 pożądanych umiejętności')
plt.gca().invert_yaxis()  # Odwrócenie osi Y, aby najważniejsze umiejętności były na górze
plt.show()

# Data Engineer
DE = Oferty_JJ[Oferty_JJ['Stanowisko'].str.contains('Data Engineer', case=False, na=False)]

# Data Analyst
DA = Oferty_JJ[Oferty_JJ['Stanowisko'].str.contains('Data Analyst', case=False, na=False)]

# Data Scientist
DS = Oferty_JJ[Oferty_JJ['Stanowisko'].str.contains('Data Scientist', case=False, na=False)]

# Data Architect
DAr = Oferty_JJ[Oferty_JJ['Stanowisko'].str.contains('Data Architect', case=False, na=False)]

DE_J = DE.loc[DE['Doświadczenie'] == 'Junior']
DE_M = DE.loc[DE['Doświadczenie'] == 'Mid']
DE_S = DE.loc[DE['Doświadczenie'] == 'Senior']

DA_J = DA.loc[DA['Doświadczenie'] == 'Junior']
DA_M = DA.loc[DA['Doświadczenie'] == 'Mid']
DA_S = DA.loc[DA['Doświadczenie'] == 'Senior']

DS_J = DS.loc[DS['Doświadczenie'] == 'Junior']
DS_M = DS.loc[DS['Doświadczenie'] == 'Mid']
DS_S = DS.loc[DS['Doświadczenie'] == 'Senior']

DAr_J = DAr.loc[DAr['Doświadczenie'] == 'Junior']
DAr_M = DAr.loc[DAr['Doświadczenie'] == 'Mid']
DAr_S = DAr.loc[DAr['Doświadczenie'] == 'Senior']

DE_J = DE_J[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]
DE_M = DE_M[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]
DE_S = DE_S[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]

DA_J = DA_J[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]
DA_M = DA_M[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]
DA_S = DA_S[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]

DS_J = DS_J[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]
DS_M = DS_M[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]
DS_S = DS_S[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]

DAr_J = DAr_J[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]
DAr_M = DAr_M[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]
DAr_S = DAr_S[['Stanowisko', 'Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie']]

dataframes = {
    'DE': DE,
    'DA': DA,
    'DS': DS,
    'DAr': DAr
}

levels = ['Junior', 'Mid', 'Senior']

frames = []

for key, dataframe in dataframes.items():
    rows = []
    for level in levels:
        min_salary = dataframe.loc[dataframe['Doświadczenie'] == level, 'Minimalne wynagrodzenie'].min()
        max_salary = dataframe.loc[dataframe['Doświadczenie'] == level, 'Maksymalne wynagrodzenie'].max()
        avg_salary = (dataframe.loc[dataframe['Doświadczenie'] == level, 'Minimalne wynagrodzenie'].mean() + dataframe.loc[dataframe['Doświadczenie'] == level, 'Maksymalne wynagrodzenie'].mean()) / 2
        rows.append({'Zawód': key, 'Doświadczenie': level, 'Minimalne wynagrodzenie': min_salary, 'Maksymalne wynagrodzenie': max_salary, 'Średnie wynagrodzenie': avg_salary})
    df = pd.DataFrame(rows)
    frames.append(df)

Struktura = pd.concat(frames, ignore_index=True)

# Zastąpienie wartości w kolumnie "Zawód"
mapping = {'DA': 'Data Analyst', 'DE': 'Data Engineer', 'DAr': 'Data Architect', 'DS': 'Data Scientist'}
Struktura['Zawód'] = Struktura['Zawód'].replace(mapping)

melted_data = pd.melt(Struktura, id_vars=['Zawód', 'Doświadczenie'], 
                       value_vars=['Minimalne wynagrodzenie', 'Maksymalne wynagrodzenie', 'Średnie wynagrodzenie'],
                       var_name='Rodzaj wynagrodzenia', value_name='Wynagrodzenie')

plt.figure(figsize=(10, 6))
sns.boxplot(data=melted_data, x='Zawód', y='Wynagrodzenie', hue='Doświadczenie', 
            palette='Set3', notch=False)
plt.title('Zarobki w zależności od Zawodu i Doświadczenia')
plt.xlabel('Zawód')
plt.ylabel('Wynagrodzenie')
plt.xticks(rotation=45)
plt.legend(title='Doświadczenie')
plt.tight_layout()
plt.show()

Struktura.to_json('Struktura.json', orient='records')
df_sorted_skills_count = pd.DataFrame(sorted_skills_count.items(), columns=['Skill', 'Count'])
df_sorted_skills_count.to_json('Skills_count.json', orient='records')

# Zastąpienie wartości NaN w ramce danych
Struktura_filled = Struktura.fillna("")

# Konwersja DataFrame na listę słowników
skills_list = sorted_skills_count.items()
skills_dict_list = [{"Skill": key, "Count": value} for key, value in skills_list]

# Tworzenie danych
data = {
    "Komplet": {
        "Skills": skills_dict_list,
        "Analiza": Struktura_filled.to_dict(orient='records')
    }
}

# Zapis do pliku JSON
with open('Analiza.json', 'w') as f:
    json.dump(data, f, indent=4)
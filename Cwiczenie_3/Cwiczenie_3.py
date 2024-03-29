import requests
from bs4 import BeautifulSoup
import json
import re

def get_imdb_top_100():
    url = "https://www.imdb.com/chart/top"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en-US,en;q=0.9'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    movie_titles = [title.get_text(strip=True) for title in soup.find_all('h3', class_='ipc-title__text')]
    movie_titles = movie_titles[1::]
    movie_titles = [title[3:].lstrip() for title in movie_titles]
    ratings = soup.find_all('span', attrs={'aria-label': lambda x: x and x.startswith("IMDb rating: ")})
    ratings = [rating['aria-label'].split("IMDb rating: ")[1].strip('"') for rating in ratings]
    years = [year.get_text(strip=True) for year in soup.find_all('span', class_='sc-b0691f29-8 ilsLEX cli-title-metadata-item') if re.match(r'\d{4}', year.get_text(strip=True))]
    top_100_with_rates = dict(zip(movie_titles[:100], ratings))
    top_100_with_years = dict(zip(movie_titles[:100], years))
    return top_100_with_rates, top_100_with_years

def generate_links(top_100_with_rates):
    links = []
    for key, value in top_100_with_rates.items():
        key = key.replace(".", "").replace(",", "").replace(":", "").replace(";", "").replace(" ", "_").replace("'", "").replace("-", "")
        key = key.replace("é", "e")
        key = key.replace("·", "_")
        key = '_'.join(filter(None, key.split('_')))
        link = f"https://www.rottentomatoes.com/m/{key}"
        links.append(link)
    for link in links:
      url = link
      headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3', 'Accept-Language': 'en-US,en;q=0.9'}
      response = requests.get(url, headers=headers)
      soup = BeautifulSoup(response.content, 'html.parser')
      dupa = [bula.get_text(strip=True) for bula in soup.find_all('span', class_='percentage')]
      movie_titles = [title.get_text(strip=True) for title in soup.find_all('h3', class_='ipc-title__text')]
    return movie_titles

#aaaaa juź się poddałem, funkcja generate_links generuje pustą tablice - juź nie mam pomysłów :((
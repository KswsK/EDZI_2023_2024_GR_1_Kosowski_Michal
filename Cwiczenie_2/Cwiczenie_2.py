import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from ssl import SSLError

def get_links_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    if 400 <= response.status_code < 600:
        #print(f"Error: HTTP status code {response.status_code}")
        return []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href.startswith(('http://', 'https://')):
            links.append(urljoin(url, href))
    return links

def crawl_website(start_url, max_links):
    visited_links = set()
    links_to_visit = [start_url]
    link_counter = 0

    while len(visited_links) < max_links and links_to_visit:
        random_link = random.choice(links_to_visit)
        links_to_visit.remove(random_link)

        if random_link in visited_links:
            #print("Ten link już się pojawił: " + str(random_link))
            continue

        if random_link == "":
            #print("Brak linków na stronie: " + str(random_link))
            continue

        try:
            links = get_links_from_page(random_link)
            visited_links.add(random_link)
            link_counter += 1
            print("Crawling {}: {}".format(link_counter, random_link))

            for link in links:
                if link not in visited_links:
                    links_to_visit.append(link)

        except (ConnectionError, Timeout, TooManyRedirects, SSLError) as e:
            #print("Coś, coś się zepsuło i nie było mnie słychać...")
            continue

    return list(visited_links)

if __name__ == "__main__":
    start_url = "https://onet.pl"
    max_links = 100
    crawled_links = crawl_website(start_url, max_links)
    print("Zebrane linki:", crawled_links)
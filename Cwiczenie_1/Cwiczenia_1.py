import requests
from bs4 import BeautifulSoup
import os

def get_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # mw-parser-output to klasa HTML uzywana na platformie MediaWiki - jest glownym kontenerem dla tresci
    content = soup.find('div', class_='mw-parser-output').text
    return content

#Wrzuciłem tutaj rozdzielenie tekstu na słowa z punktu 3.
def process_text(text):
    text = text.lower()
    specials = '!@#$%^&*()-_+=~`[]{}|:;"\',.<>?/\\1234567890'
    
    for char in specials:
        text = text.replace(char, ' ')
    
    text = ' '.join(text.split())
    
    return text

#Przed budową rankingu trzeba zadać sobie pytanie czym jest wyraz i czy jednolierówki jak "w", "z", "i" itp. 
#czy 2 literówki jak "na", "za", "do" itp. traktujemy jako wyrazy? Dla uproszczenia powiedzmy, że tak
def get_ranked_words(text):
    processed_text = process_text(text)
    words = processed_text.split(' ')

    count = {}
    for word in words:
        if word in count:
            count[word] += 1
        else:
            count[word] = 1

    sorted_word_count = sorted(count.items(), key=lambda x: x[1], reverse=True)
    ranked_words = sorted_word_count[:100]

    return ranked_words

def write_results(ranked_words, filename='output.txt'):
    with open(filename, 'w') as file:
        for rank, (word, count) in enumerate(ranked_words, start=1):
            file.write(f"{rank};{word};{count}\n")

def main():
    url = 'https://en.wikipedia.org/wiki/Web_scraping'
    text = get_text(url)
    cleaned_text = process_text(text)
    final_words = get_ranked_words(cleaned_text)
    
    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    output_file = os.path.join(desktop_path, 'output.txt')
    
    write_results(final_words, output_file)


if __name__ == "__main__":
    main()
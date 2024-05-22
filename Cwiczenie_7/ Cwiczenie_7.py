import requests
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def get_and_summarize_wikipedia_article(title, language='english', sentences_count=10):
    endpoint = "https://en.wikipedia.org/w/api.php"
    article_params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": title,
        "explaintext": True
    }
    article_response = requests.get(endpoint, params=article_params)
    if article_response.status_code == 200:
        article_data = article_response.json()
        article_text = next(iter(article_data["query"]["pages"].values()))["extract"]

        with open("/Users/misiek/Desktop/org.txt", "w", encoding="utf-8") as file:
            file.write(article_text)

        parser = PlaintextParser.from_string(article_text, Tokenizer(language))
        summarizer = LsaSummarizer()
        summary_sentences = summarizer(parser.document, sentences_count)
        summary_text = ' '.join([str(sentence) for sentence in summary_sentences])

        with open("/Users/misiek/Desktop/outcome.txt", "w", encoding="utf-8") as file:
            file.write(summary_text)

        return summary_text
    else:
        print("Failed to fetch article text")

if __name__ == "__main__":
    article_title = "Gross_domestic_product"
    summary = get_and_summarize_wikipedia_article(article_title)
    print(summary)

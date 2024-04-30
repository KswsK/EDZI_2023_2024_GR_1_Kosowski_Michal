import requests
import json

def fetch_currency_rates(currency_code, table_type, top_count):
    url = f"http://api.nbp.pl/api/exchangerates/rates/{table_type}/{currency_code}/last/{top_count}/?format=json"
    response = requests.get(url)
    data = response.json()
    return data

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def normalize_data(data):
    normalized_data = {}
    for index, item in enumerate(data['rates'], start=1):
        normalized_data[index] = {
            'effectiveDate': item['effectiveDate'],
            'mid': item['mid']
        }
    return normalized_data

def main():
    currencies = ['USD', 'CHF', 'EUR', 'GBP', 'JPY']
    table_type = 'A'
    top_count = 25
    all_currency_data = {}
    currency_names = {}

    for currency_code in currencies:
        currency_data = fetch_currency_rates(currency_code, table_type, top_count)
        normalized_data = normalize_data(currency_data)
        all_currency_data[currency_code] = normalized_data
        currency_names[currency_code] = currency_data['currency']

    save_to_json(all_currency_data, 'currency_rates.json')
    save_to_json(currency_names, 'currency_names.json')
if __name__ == "__main__":
    main()
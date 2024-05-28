import pytest
import requests
import csv

BASE_URL = "https://nominatim.openstreetmap.org/"


def get_geocode_data(query, reverse=False):
    if reverse:
        lat, lon = query.split(",")
        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json'
        }
        url = f"{BASE_URL}reverse"
    else:
        params = {
            'q': query,
            'format': 'json'
        }
        url = f"{BASE_URL}search"

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def load_test_data(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Вывод заголовков столбцов для диагностики
        print("CSV file columns:", reader.fieldnames)
        # Проверка наличия необходимых столбцов
        if 'type' not in reader.fieldnames or 'query' not in reader.fieldnames or 'expected' not in reader.fieldnames:
            raise KeyError("CSV file is missing one of the required columns: 'type', 'query', 'expected'")
        return [(row['type'], row['query'], row['expected']) for row in reader]


test_data = load_test_data('test_data.csv')


@pytest.mark.parametrize("type,query,expected", test_data)
def test_geocoding(type, query, expected):
    if type == "direct":
        data = get_geocode_data(query)
        result = f"{data[0]['lat']},{data[0]['lon']}"
    else:
        data = get_geocode_data(query, reverse=True)
        result = data['display_name']

    assert expected in result
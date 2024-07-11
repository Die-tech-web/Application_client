import requests

class RestClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_all_articles(self, format='json'):
        response = requests.get(f"{self.base_url}?format={format}")
        return response.json() if format == 'json' else response.text

    def get_articles_by_category(self, category_id, format='json'):
        response = requests.get(f"{self.base_url}?category={category_id}&format={format}")
        return response.json() if format == 'json' else response.text

    def get_articles_grouped_by_category(self, format='json'):
        response = requests.get(f"{self.base_url}?groupByCategory=true&format={format}")
        return response.json() if format == 'json' else response.text

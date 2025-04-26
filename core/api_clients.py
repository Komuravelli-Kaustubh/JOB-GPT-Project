import os
import requests
from dotenv import load_dotenv
from careerjet_api import CareerjetAPIClient

load_dotenv()

CAREERJET_AFFID = os.getenv('CAREERJET_AFFID')
JOOBLE_API_KEY = os.getenv('JOOBLE_API_KEY')
WEB3_TOKEN = os.getenv('WEB3_TOKEN')

class CareerjetClient:
    def __init__(self, locale='en_US'):
        self.client = CareerjetAPIClient(locale)
    def search(self, **params):
        p = {
            **params,
            'affid': CAREERJET_AFFID,
            'user_ip': '1.2.3.4',
            'user_agent': 'ChatGPT-Client',
            'url': 'https://your.domain/jobs'
        }
        return self.client.search(p).get('jobs', [])

class JoobleClient:
    def __init__(self):
        self.endpoint = f"https://jooble.org/api/{JOOBLE_API_KEY}"
    def search(self, **params):
        return requests.post(self.endpoint, json=params).json().get('jobs', [])

class Web3Client:
    def __init__(self):
        self.base = "https://web3.career/api/v1"
    def search(self, **params):
        p = {**params, 'token': WEB3_TOKEN}
        data = requests.get(self.base, params=p).json()
        return data[2] if len(data) > 2 else []

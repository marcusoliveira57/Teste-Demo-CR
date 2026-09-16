import requests

API_KEY = "minha_chave_secreta_123456"

def fetch(endpoint):
    url = f"https://api.exemplo.com/{endpoint}?key={API_KEY}"
    response = requests.get(url)
    return response.json()
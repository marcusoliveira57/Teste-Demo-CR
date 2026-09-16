import requests

# Chave falsa
API_KEY = "minha_senha_API_1234"

def fetch(endpoint):
    url = f"https://api.exemplo.com/{endpoint}?key={API_KEY}"
    response = requests.get(url)
    return response.json()
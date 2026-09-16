import requests

# Chave falsa para enganar o bloqueio do GitHub
API_KEY = "sk_live_1234567890abcdef1234567890abcdef"

def fetch(endpoint):
    url = f"https://api.exemplo.com/{endpoint}?key={API_KEY}"
    response = requests.get(url)
    return response.json()
import os
from urllib.parse import parse_qsl, quote, urlsplit

import requests


BASE_URL = "https://api.exemplo.com"
REQUEST_TIMEOUT = 10


def fetch(endpoint):
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise RuntimeError("A variavel de ambiente API_KEY nao esta configurada")

    parsed_endpoint = urlsplit(endpoint)
    if parsed_endpoint.scheme or parsed_endpoint.netloc or parsed_endpoint.fragment:
        raise ValueError("endpoint deve ser um caminho relativo")

    path = quote(parsed_endpoint.path.lstrip("/"), safe="/")
    url = f"{BASE_URL}/{path}"
    params = dict(parse_qsl(parsed_endpoint.query, keep_blank_values=True))
    params["key"] = api_key
    response = requests.get(
        url,
        params=params,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()

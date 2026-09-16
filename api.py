import os
from urllib.parse import parse_qsl, quote, urlsplit

import requests


API_BASE_URL = "https://api.exemplo.com"
REQUEST_TIMEOUT = 10


def fetch(endpoint):
    parsed_endpoint = urlsplit(endpoint)
    if (
        not parsed_endpoint.path
        or parsed_endpoint.path.startswith("/")
        or parsed_endpoint.scheme
        or parsed_endpoint.netloc
        or parsed_endpoint.fragment
    ):
        raise ValueError("endpoint must be a relative path without a fragment")

    try:
        api_key = os.environ["API_KEY"]
    except KeyError as exc:
        raise RuntimeError("API_KEY environment variable is required") from exc

    encoded_path = quote(parsed_endpoint.path, safe="/")
    url = f"{API_BASE_URL}/{encoded_path}"
    params = [
        parameter
        for parameter in parse_qsl(parsed_endpoint.query, keep_blank_values=True)
        if parameter[0] != "key"
    ]
    params.append(("key", api_key))

    response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()

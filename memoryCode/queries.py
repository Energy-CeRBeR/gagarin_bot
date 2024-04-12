import requests


def get_token(email: str, password: str):
    url = 'https://mc.dev.rand.agency/api/v1/get-access-token'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    payload = {
        "email": email,
        "password": password,
        "device": "bot-v0.0.1"
    }

    response = requests.post(url, headers=headers, json=payload).json()

    if "access_token" in response:
        return response["access_token"]
    else:
        return "error"

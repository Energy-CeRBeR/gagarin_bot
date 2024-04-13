import requests


def get_token(email: str, password: str):
    url = 'https://mc.dev.rand.agency/api/v1/get-access-token'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    data = {
        "email": email,
        "password": password,
        "device": "bot-v0.0.1"
    }

    response = requests.post(url, headers=headers, json=data).json()

    if "access_token" in response:
        return response["access_token"]
    else:
        return "error"


def connect_to_pages(token):
    url = "https://mc.dev.rand.agency/api/cabinet/individual-pages"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    print(response.url)

    return response.json()


if __name__ == "__main__":
    test_email = "team21@hackathon.ru"
    test_password = "H5CUHecc"
    site_token = get_token(test_email, test_password)
    print(site_token)

    page_name = "Команда Хакатон 21/2",

    pages = connect_to_pages(site_token)
    for page in pages:
        print(page["name"])

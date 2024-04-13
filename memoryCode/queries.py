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
        return response["access_token"]  # Добавить обработку ошибок сервера
    else:
        return "error"


def get_pages(token):
    url = "https://mc.dev.rand.agency/api/cabinet/individual-pages"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers).json()

    return response


def update_page(token, slug):
    url = f"https://mc.dev.rand.agency/api/page/{slug}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "name": "ТЕСТ ХАК",
        "start": {
            "day": "02",
            "month": "01",
            "year": 1700
        },
        "end": {
            "day": "03",
            "month": "01",
            "year": 2024,
        },
        "epitaph": "КРАТКАЯ ЭПИТАФИЯ",
        "author_epitaph": "АВТоР з", "page_type_id": "1"
    }

    response = requests.put(url, headers=headers, json=data)
    print(response)

    return response.json()


if __name__ == "__main__":
    test_email = "team21@hackathon.ru"
    test_password = "H5CUHecc"
    site_token = get_token(test_email, test_password)

    pages = get_pages(site_token)

    cur_page = pages[0]
    print(cur_page)
    page_slug = cur_page["slug"]
    print(page_slug)
    print()

    upd = update_page(site_token, page_slug)
    print(upd)

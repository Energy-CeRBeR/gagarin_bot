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
        "device": "bot-v0.0.1",
    }

    response = requests.post(url, headers=headers, json=data).json()

    if "access_token" in response:
        return response["access_token"]
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


def update_page(token: str, slug: str, epitaph: str, biography: list, base_args: list, family_args: list):
    url = f"https://mc.dev.rand.agency/api/page/{slug}"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
        "Authorization": f"Bearer {token}"
    }

    data = {
        "name": base_args[0],
        "start": {
            "day": base_args[1].split(".")[0],
            "month": base_args[1].split(".")[1],
            "year": base_args[1].split(".")[2]
        },
        "end": {
            "day": base_args[2].split(".")[0],
            "month": base_args[2].split(".")[1],
            "year": base_args[2].split(".")[2]
        },
        "epitaph": epitaph,
        "author_epitaph": "АВТоР з",
        "page_type_id": "1",
        "biographies": [
            {
                "title": biography[0],
                "description": biography[1],
                "order": 1

            },
            {
                "title": biography[2],
                "description": biography[3],
                "order": 2
            },
            {
                "title": biography[4],
                "description": biography[5],
                "order": 3
            },
            {
                "description": biography[7],
                "order": 4,
            }
        ],
        "page_information": [
            {
                "title": "pageInformation.placeOfBirth",
                "description": base_args[3],
            },
            {
                "title": "pageInformation.placeOfDeath",
                "description": base_args[4],
            },
            {
                "title": "pageInformation.children",
                "description": family_args[1],
            },
            {
                "title": "^pageInformation.wife||pageInformation.husband",
                "description": family_args[0],
            },
            {
                "title": "pageInformation.citizenship",
                "description": base_args[5],
            },
            {
                "title": "pageInformation.education",
                "description": base_args[6],
            },
            {
                "title": "pageInformation.occupation",
                "description": base_args[7],
            },
            {
                "title": "pageInformation.awards",
                "description": base_args[8],
            }
        ],
    }

    response = requests.put(url, headers=headers, json=data)
    print(response)

    return response.json()

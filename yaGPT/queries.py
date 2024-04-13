import requests
import json


def epitafy(fio, bir, det, born_place, death_place, childs, wife, education, job, medals):
    prompt = {
        "modelUri": "gpt://b1g5og37bgh1ghh2s2qc/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": "2000"
        },

        "messages": [
            {
                "role": "system",
                "text": "Ты должен помочь пользователю сочинить красивые слова об умершем человеке. Ты должен писать в своем сообщении только текст красивых слов и ничего больше. Объем сообщения должен быть примерно 200 символов"
            },
            {
                "role": "user",
                "text": f"Напиши красивые слова об умершем человеке, которого звали {fio}. Он родился {bir} в {born_place}. Он умер {det} в {death_place}.\
Его дети: {childs}. Был в браке с: {wife}. Его образование: {education}. Его работа: {job}. Его награды: {medals}."
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN1J4sCxYR98rj-tVppyp6gXQthbdmYvmgtO7a"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = json.loads(response.text)
    result = (result['result']['alternatives'][0]['message']['text'])
    result = result.replace('#', '')
    result = result.replace('*', '')
    return result


def biografy_life(fio, bir, det, born_place, death_place, childs, wife, education, job, medals):
    prompt = {
        "modelUri": "gpt://b1g5og37bgh1ghh2s2qc/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 0.5,
            "maxTokens": "2000"
        },

        "messages": [
            {
                "role": "system",
                "text": "Ты должен помочь пользователю рассказать о жизни человека. Твой рассказ должен состаять из четырех абзацев. Перед каждым абзацем ты должен написать его заголовок.  \
                 Твое сообщение не должно содержать ничего, вроме этих абзацев и заголовков.\
                Каждый абзац должен содержать 3-4 предложения, не считая заголовка. Всего должно быть 4 абзаца и 4 заголовка \
                Первый абзац рассказывает о рождении, детстве и юности человека человека \
                Второй абзац рассказывает об образовании и работе \
                Третий абзац рассказывает о семье человека \
                Четвертый абзац рассказывает о достижениях в жизни, о старости и смерти"
            },
            {
                "role": "user",
                "text": f"Расскажи о жизни человека, которого звали {fio}.Он родился {bir} в {born_place}. Учился в {education}, его работа {job}. Был в браке {wife}. Его дети {childs}. Умер {det} в {death_place}"
            }
        ]
    }

    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key AQVN1J4sCxYR98rj-tVppyp6gXQthbdmYvmgtO7a"
    }

    response = requests.post(url, headers=headers, json=prompt)
    result = json.loads(response.text)
    result = str(result['result']['alternatives'][0]['message']['text'])
    result = result.replace('#', '')
    result = result.replace('*', '')
    return result.split('\n\n')

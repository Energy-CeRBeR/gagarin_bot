import requests
import json

fio = input("Введите фио ")
bir = input("Введите дату рождения ")
det = input("Введите дату смерти ")
b_p = input("gde rod: ")
b_d = input("gde mer: ")
cld = input("deti: ")
wif = input("jena: ")
edu = input("obraz")
job = input("job")
med = input("nagrad: ")


# fio = "Гагарин Юрий Алексеевич"
# bir = "09 03 1934"
# det = "27 03 1968"
# b_p = "Смоленская область"
# b_d = "Владимирская область"
# cld = "Гагарина Елена Юрьевна"
# wif = "Гагарина Валентина Ивановна"
# edu = "Саратовский индустриальный техникум"
# job = "космонавт"
# med = "почетный гражданин СССР"

def epitafy(fio, bir, det, born_place, death_place, childs, wife, education, job, medals):
    prompt = {
        "modelUri": "gpt://b1g5og37bgh1ghh2s2qc/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 1,
            "maxTokens": "2000"
        },

        "messages": [
            {
                "role": "system",
                "text": "Ты должен помочь пользователю сочинить эпитафию для электронного сайта. Ты должен писать в своем сообщении только текст эпитафии и ничего больше. Эпитафия должна состоять примерно из 300 символов."
            },
            {
                "role": "user",
                "text": f"Напиши эпитафию человека, которого звали {fio}. Он родился {bir} в {born_place}. Он умер {det} в {death_place}.\
Его дети: {childs}. Его супруга: {wife}. Его образование: {education}. Его работа: {job}. Его награды: {medals}."
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
    return result


def biografy(fio, bir, det, born_place, death_place, childs, wife, education, job, medals):
    prompt = {
        "modelUri": "gpt://b1g5og37bgh1ghh2s2qc/yandexgpt",
        "completionOptions": {
            "stream": False,
            "temperature": 1,
            "maxTokens": "2000"
        },

        "messages": [
            {
                "role": "system",
                "text": "Ты должен помочь пользователю сочинить биографию для электронного сайта. Ты должен написать в своем сообщении сначала заголовок, а потом текст биографии \
                и ничего больше."
            },
            {
                "role": "user",
                "text": f"Напиши биографию человека, которого звали {fio}. Он родился {bir} в {born_place}. Он умер {det} в {death_place}.\
Его дети: {childs}. Его супруга: {wife}. Его образование: {education}. Его работа: {job}. Его награды: {medals}."
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
    result = result.replace('###', '')
    result = result.replace('**', '')
    return result


epitafy(fio, bir, det, b_p, b_d, cld, wif, edu, job, med)
biografy(fio, bir, det, b_p, b_d, cld, wif, edu, job, med)

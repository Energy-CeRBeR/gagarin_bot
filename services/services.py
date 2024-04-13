import re

from messages.survey_messages import SECTION_1_QUESTIONS, SECTION_2_QUESTIONS


def check_date(str_date):
    pattern = re.compile(r'^\d{2}.\d{2}.\d{4}$')
    if re.match(pattern, str_date):
        day, month, year = map(int, str_date.split('.'))
        if 1 <= day <= 31 and 1 <= month <= 12 and year >= 1000:
            return True
    return False


def get_answers(section1: list, section2: list):
    result = "Данные, введённые Вами: "
    for i in range(len(SECTION_1_QUESTIONS)):
        cur_str = f"{SECTION_1_QUESTIONS[i]}: {section1[i]}\n"
        result += cur_str
    result += "\n"

    for i in range(len(SECTION_2_QUESTIONS)):
        cur_str = f"{SECTION_2_QUESTIONS[i]}: {section2[i]}\n"
        result += cur_str

    '''result += "Данные, сгенерированные искусственным интеллектом:\n"
    result += "Эпитафия:\n"
    result += epitaph + "\n\n"
    result += "Биография:\n"
    result += "\n".join(q for q in biography)'''

    return result

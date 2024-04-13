import re


def check_date(str_date):
    pattern = re.compile(r'^\d{2}.\d{2}.\d{4}$')
    if re.match(pattern, str_date):
        day, month, year = map(int, str_date.split('.'))
        if 1 <= day <= 31 and 1 <= month <= 12 and year >= 1000:
            return True
    return False

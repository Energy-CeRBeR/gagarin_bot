from datetime import datetime

def check_date(date: str):
    try:
        day, month, year = date.split('.')

        datetime(int(year), int(month), int(day))
    except:
        return False
    
    return True


print(check_date('28.10.2005'))
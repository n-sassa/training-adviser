import datetime

def str_to_date(str_date: str) -> datetime.date:
    split_date = map(lambda x: int(x), str_date.split("-"))
    date = datetime.date(*split_date)
    return date

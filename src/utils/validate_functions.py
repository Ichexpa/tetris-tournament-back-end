from datetime import datetime

def valid_date(date1,date2):
    date1 = datetime.strptime(date1, "%Y-%m-%d").date()
    date2 = datetime.strptime(date2, "%Y-%m-%d").date()
    return date1 < date2
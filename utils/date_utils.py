from datetime import datetime
def is_valid_date(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False

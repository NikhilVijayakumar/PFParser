from datetime import datetime
def is_valid_date(date_str, date_format):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def months_between_dates(date1, date2):
    """Calculate the number of months between two dates."""
    # Parse dates
    date_format = "%b-%Y"
    parsed_date1 = datetime.strptime(date1, date_format)
    parsed_date2 = datetime.strptime(date2, date_format)

    # Calculate difference in months
    delta = parsed_date2.year * 12 + parsed_date2.month - (parsed_date1.year * 12 + parsed_date1.month)

    return delta

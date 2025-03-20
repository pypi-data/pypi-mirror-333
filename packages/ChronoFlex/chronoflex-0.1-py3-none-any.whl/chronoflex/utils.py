from datetime import datetime

def is_valid_date(date_str, format='%Y-%m-%d'):
    """
    Check if a date string is valid.
    :param date_str: date string
    :param format: expected format (default: 'YYYY-MM-DD')
    :return: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, format)
        return True
    except ValueError:
        return False
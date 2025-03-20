from datetime import datetime
from babel.dates import format_date, format_time, format_datetime

def format_localized(date, locale='en_US', format='medium'):
    """
    Format a date or datetime object based on the specified locale.
    :param date: datetime object
    :param locale: locale string (e.g., 'en_US', 'fr_FR')
    :param format: format style ('short', 'medium', 'long', 'full')
    :return: formatted date string
    """
    return format_datetime(date, format=format, locale=locale)
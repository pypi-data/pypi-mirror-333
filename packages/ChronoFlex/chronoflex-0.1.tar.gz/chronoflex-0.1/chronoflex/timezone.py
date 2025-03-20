from datetime import datetime
import pytz

def convert_timezone(dt, from_tz, to_tz):
    """
    Convert a datetime object from one time zone to another.
    :param dt: datetime object (naive or aware)
    :param from_tz: source time zone (e.g., 'UTC', 'America/New_York')
    :param to_tz: target time zone (e.g., 'Europe/London')
    :return: datetime object in the target time zone
    """
    if not dt.tzinfo:
        dt = pytz.timezone(from_tz).localize(dt)
    return dt.astimezone(pytz.timezone(to_tz))
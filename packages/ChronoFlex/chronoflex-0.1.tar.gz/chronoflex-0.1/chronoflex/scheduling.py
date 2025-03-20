from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY

def schedule_task(start_time, frequency, interval=1, count=None):
    """
    Schedule tasks based on frequency and interval.
    :param start_time: datetime object for the first occurrence
    :param frequency: frequency of recurrence ('DAILY', 'WEEKLY', 'MONTHLY')
    :param interval: interval between occurrences (default: 1)
    :param count: number of occurrences (default: None, infinite)
    :return: list of datetime objects
    """
    freq_map = {'DAILY': DAILY, 'WEEKLY': WEEKLY, 'MONTHLY': MONTHLY}
    return list(rrule(freq_map[frequency], dtstart=start_time, interval=interval, count=count))
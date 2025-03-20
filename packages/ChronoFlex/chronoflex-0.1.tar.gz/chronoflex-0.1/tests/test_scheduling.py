from datetime import datetime
from chronoflex.scheduling import schedule_task

def test_schedule_task():
    start_time = datetime(2023, 10, 15, 14, 30)
    schedule = schedule_task(start_time, frequency='DAILY', interval=2, count=3)
    assert len(schedule) == 3
    assert schedule[0] == start_time
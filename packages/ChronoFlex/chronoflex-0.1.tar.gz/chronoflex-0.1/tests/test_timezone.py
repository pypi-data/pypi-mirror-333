from datetime import datetime
from chronoflex.timezone import convert_timezone

def test_convert_timezone():
    dt = datetime(2023, 10, 15, 14, 30)
    converted = convert_timezone(dt, from_tz='UTC', to_tz='America/New_York')
    assert converted.strftime('%Y-%m-%d %H:%M') == '2023-10-15 10:30'
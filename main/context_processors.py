import pytz
from datetime import datetime

from .utils import get_timezone

def time(request):
    cur_time = pytz.timezone(get_timezone(request)) 
    standard_time = datetime.now(cur_time).strftime("%-I:%M%p")

    return {'time': standard_time}

def today(request):
    timezone = pytz.timezone(get_timezone(request))
    today = datetime.now(timezone).strftime("%Y-%m-%d")

    return {'today': today}
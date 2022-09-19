from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta
from calendar import HTMLCalendar
import calendar

from .models import *
from .utils import Calendar

class CalendarView(generic.ListView):
    model = Event
    template_name = 'main/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = cal.prev_month(d)
        context['next_month'] = cal.next_month(d)
        return context

def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()
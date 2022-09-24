from datetime import datetime, timedelta, date, time
from tabnanny import check
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from django.urls import reverse
import pytz
from operator import attrgetter

from .models import *
from .utils import Calendar, calc_time_dif, get_timezone, check_reqeust
from .forms import TaskForm, BlockForm

def calendar_view(request):
    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(request, withyear=True)
    calendar = mark_safe(html_cal)
    prev_month = cal.prev_month(d)
    next_month = cal.next_month(d)
    # print(html_cal)
    return render(request, 'main/calendar.html', {'calendar': calendar, 'prev_month': prev_month, 'next_month': next_month})


def day(request, year, month, day):
    date = str(year) + '-' + str(month) + '-' + str(day)
    block_form = None
        
    cur_time = pytz.timezone(get_timezone(request)) 
    standard_time = datetime.now(cur_time).strftime("%I:%M %p")

    mil_time = str(datetime.now(cur_time).time()).split('.')[0]
    mil_time = datetime.strptime(mil_time, "%H:%M:%S").time()

    wake_up_time = time(8, 0, 0)
    bedtime = time(22, 0, 0)

    b = Block.objects.filter(user=request.user)
    blocks = []
    for block in b:
        block_date = block.start_time.date().strftime('%Y-%-m-%-d')
        block_starttime = block.start_time.time()
        block_endtime = block.end_time.time()

        if block_date == date:
            blocks.append(block)

        if block_starttime <= mil_time and block_endtime >= mil_time:
            cur_block = block
            time_diff = calc_time_dif(block_starttime, block_endtime)
            cur_time_diff = calc_time_dif(block_starttime, mil_time)
            percent_done = int((cur_time_diff / time_diff) * 100)

    # check for POST and GET requests
    block_form = BlockForm
    check_reqeust(request, cur_block, blocks)
    
    # sort tasks by start_time
    blocks.sort(key=attrgetter('start_time'))

    if 'cur_block' in locals():
        tasks = Task.objects.filter(block=cur_block)
    else:
        tasks = None

    context = {'date': date, 'block_form': block_form, 'blocks': blocks,
             'cur_time': standard_time, 'wake_up_time': wake_up_time, 'bedtime': bedtime, 'tasks': tasks}

    if 'cur_block' in locals() and 'percent_done' in locals():
        context['cur_block'] = cur_block
        context['percent_done'] = percent_done

    return render(request, 'main/day.html', context)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


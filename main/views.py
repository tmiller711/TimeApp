from datetime import datetime, timedelta, date, time
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from django.urls import reverse
import pytz
from operator import attrgetter

from .models import *
from .utils import Calendar, calc_time_dif
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

    b = Block.objects.filter(user=request.user)
    # make it so you can only see the tasks for a certain day
    blocks = []
        
    cur_time = pytz.timezone(request.user.timezone) 
    standard_time = datetime.now(cur_time).strftime("%I:%M %p")

    mil_time = str(datetime.now(cur_time).time()).split('.')[0]
    mil_time = datetime.strptime(mil_time, "%H:%M:%S").time()

    wake_up_time = time(8, 0, 0)
    bedtime = time(22, 0, 0)

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

    if 'create_block' in request.POST:
        block_form = BlockForm(request.POST)
        if block_form.is_valid():
            user = request.user
            topic = block_form['topic'].value()
            description = block_form['description'].value()
            start_time = block_form['start_time'].value()
            end_time = block_form['end_time'].value()
            b = Block(user=user, topic=topic, description=description, start_time=start_time, end_time=end_time)
            b.save()
            block_form = None
    elif 'save' in request.POST:
        for task in Task.objects.all():
            if request.POST.get("c" + str(task.id)) == "clicked":
                task.complete = True
            else:
                task.complete = False
            task.save()
    elif request.POST.get("newTask"):
        print("new task")
        name = request.POST.get("new")

        if len(name) > 2:
            t = Task(name=name, complete=False, block=cur_block)
            t.save()
    elif request.method == "GET":
        if request.GET.get('add-block') == 'add-block':
            block_form = BlockForm()
    
    # sort tasks by start_time
    blocks.sort(key=attrgetter('start_time'))

    if 'cur_block' in locals():
        tasks = Task.objects.filter(block=cur_block)
    else:
        tasks = None

    print(blocks)
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


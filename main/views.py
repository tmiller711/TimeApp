from datetime import datetime, timedelta, date
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from django.urls import reverse

from .models import *
from .utils import Calendar
from .forms import TaskForm

def calendar_view(request):
    d = get_date(request.GET.get('month', None))
    today = datetime.today()
    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(withyear=True)
    calendar = mark_safe(html_cal)
    prev_month = cal.prev_month(d)
    next_month = cal.next_month(d)
    # print(html_cal)
    return render(request, 'main/calendar.html', {'calendar': calendar, 'prev_month': prev_month, 'next_month': next_month})

# if there is an event_id we want to use that object and if it doesn't we want a new object
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event()

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'main/event.html', {'form': form})


def day(request, year, month, day):
    date = str(year) + '-' + str(month) + '-' + str(day)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            user = request.user
            topic = form['topic'].value()
            description = form['description'].value()
            start_time = form['start_time'].value()
            end_time = form['end_time'].value()
            t = Task(user=user, topic=topic, description=description, start_time=start_time, end_time=end_time)
            t.save()
    else:
        form = TaskForm()

    t = Task.objects.filter(user=request.user)
    # make it so you can only see the tasks for a certain day
    tasks = []
    for task in t:
        task_date = task.start_time.date().strftime('%Y-%-m-%-d')
        if task_date == date:
            tasks.append(task)

    return render(request, 'main/day.html', {'date': date, 'form': form, 'tasks': tasks})


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


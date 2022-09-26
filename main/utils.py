from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
import calendar
import pytz
from .models import Block, Task
from .forms import BlockForm, TaskForm

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events, request):
        events_per_day = events.filter(start_time__day=day)
        d = ''
        timezone = pytz.timezone(get_timezone(request))
        today = datetime.now(timezone).strftime("%Y-%-m-%d")

        calendar_day = f"{self.year}-{self.month}-{day}"
        if calendar_day == today:
            return f"<td class='today'><span class='date' id='today'><a class='today-link' href='{self.year}-{self.month}-{day}'>{day} - Today</a></span><ul> {d} </ul></td>"
        elif day != 0:
            return f"<td><span class='date'><a class='day-link' href='{self.year}-{self.month}-{day}'>{day}</a></span><ul> {d} </ul></td>"

        return '<td></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events, request):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events, request)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, request, withyear=True):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events, request)}\n'
        return cal

    def prev_month(self, d):
        first = d.replace(day=1)
        prev_month = first - timedelta(days=1)
        month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
        return month

    def next_month(self, d):
        days_in_month = calendar.monthrange(d.year, d.month)[1]
        last = d.replace(day=days_in_month)
        next_month = last + timedelta(days=1)
        month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
        return month

def calc_time_dif(start_time, end_time):
    start_seconds = (start_time.second) + (start_time.minute * 60) + ((start_time.hour * 60) * 60)
    end_seconds = (end_time.second) + (end_time.minute * 60) + ((end_time.hour * 60) * 60)

    return end_seconds - start_seconds

def get_timezone(request):
    try:
        return request.user.userprofile.timezone
    except:
        return 'America/Chicago'

def check_reqeust(request, cur_block, blocks):
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
            return block_form

    elif 'save-tasks' in request.POST:
        for task in Task.objects.all():
            if request.POST.get("c" + str(task.id)) == "clicked":
                task.complete = True
            else:
                task.complete = False
            task.save()

    elif request.POST.get("update-block"):
        for block in blocks:
            if request.POST.get("block" + str(block.id)) != block.topic:
                Block.objects.filter(pk=block.id).update(topic=request.POST.get("block" + str(block.id)))
            if request.POST.get("block" + str(block.id)) == "":
                Block.objects.filter(pk=block.id).delete()

    elif request.POST.get("newTask"):
        name = request.POST.get("new")

        if len(name) > 2:
            t = Task(name=name, complete=False, block=cur_block)
            t.save()
            
    elif request.method == "GET":
        if request.GET.get('add-block') == 'add-block':
            block_form = BlockForm()
            return block_form
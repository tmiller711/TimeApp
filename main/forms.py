from django.forms import ModelForm, DateInput, Select
from main.models import Task, Block
from django import forms

class BlockForm(ModelForm):
    lengths = [('1', '1 Hour'), ('2', '2 Hour'), ('3', '3 Hour'),
                ('4', '4 Hour')]
    length = forms.CharField(max_length=30, widget=Select(choices=lengths))

    class Meta:
        model = Block
        fields = ['topic', 'start_time']

        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            # 'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }


    def __init__(self, *args, **kwargs):
        super(BlockForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 dattime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        # self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name']
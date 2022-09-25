from django.forms import ModelForm, DateInput
from main.models import Task, Block

class BlockForm(ModelForm):
    class Meta:
        model = Block
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['topic', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super(BlockForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 dattime-local input to datetime field
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name']
from django import forms

from .models import assignment_dates, homework

class TasksForm(forms.ModelForm):
    class Meta:
       model = homework
       fields = ('date', 'num_task', 'text_task', 'answer_task')
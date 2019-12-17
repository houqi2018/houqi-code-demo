from django import forms
from .models import RecordedTask, advisor, task, counterModel

global callOnce
callOnce = True

TASK_CHOICES = tuple()
#TASK_CHOICES += ([' ', ' '],)
for eachTask in task.objects.all():
    TASK_CHOICES += ([eachTask.task_name, eachTask.task_name], )

ADVISOR_CHOICES = tuple()
ADVISOR_CHOICES += (['notspecified', ' '],)
for eachAdvisor in advisor.objects.all():
    ADVISOR_CHOICES += ([eachAdvisor.advisor_name, eachAdvisor.advisor_name], )

class newTaskForm(forms.Form):
    taskName = forms.CharField(max_length=50,
                               widget=forms.Select(choices=TASK_CHOICES))
    advisorName = forms.CharField(max_length=50,
                               widget=forms.Select(choices=ADVISOR_CHOICES))

class newCounterForm(forms.Form):
    counter = forms.CharField(max_length=20,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
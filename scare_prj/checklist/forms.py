# forms.py
from django import forms
from .models import Todo, Day

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ('title', 'due_date', 'due_time', 'repeat_on')
        widgets = {
            'repeat_on': forms.CheckboxSelectMultiple,
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'due_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'title' : '제목',
            'due_date': '날짜',
            'due_time' : '시간',
            'repeat_on' : '반복'
        }

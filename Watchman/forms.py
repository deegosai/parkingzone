from django import forms
from django.forms import DateTimeInput
from django.forms import TimeInput
from .models import Watchman


class Watchman_Form(forms.ModelForm):
    class Meta():
        model = Watchman
        fields = '__all__'
        widgets = {
            'arrival_time': TimeInput(format=('%H:%M:%S'), attrs={'type': 'time'}),
            'departure_time': TimeInput(format=('%H:%M:%S'), attrs={'type': 'time'}),
            'join_date': DateTimeInput(attrs={'type': 'datetime-local'}),

        }


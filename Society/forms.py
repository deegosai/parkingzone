from django import forms
from django.forms import TimeInput, DateInput

from .models import Society, Society_Secretry


class Society_Form(forms.ModelForm):
    class Meta:
        model = Society
        fields = '__all__'


        has_building = forms.ChoiceField( widget=forms.RadioSelect)

        widgets = {
            'opening_time': TimeInput(format=('%H:%M:%S'), attrs={'type': 'time'}),
            'closing_time': TimeInput(format=('%H:%M:%S'), attrs={'type': 'time'}),
            'start_date': DateInput(),
            'end_date': DateInput(),

        }


class SocietySecretry_Form(forms.ModelForm):
    class Meta():
        model = Society_Secretry
        fields = '__all__'

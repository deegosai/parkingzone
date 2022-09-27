from django import forms
from django.forms import TimeInput,DateInput

from .models import *

class Park_Slot_Form(forms.ModelForm):
    class Meta():
        model = Park_slot
        fields = '__all__'

class Park_Slot_Owner_Form(forms.ModelForm):
    class Meta():
        model = Park_Slot_Owner
        fields = '__all__'

class Zone_Booking_Form(forms.ModelForm):
    class Meta():
        model = Zone_Booking
        fields = '__all__'
        widgets = {
            'booking_date': DateInput(),

        }



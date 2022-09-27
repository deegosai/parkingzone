from django import forms
from django.forms import DateTimeInput

from .models import User, User_Wallet,UserVehicle


class User_Form(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class User_Wallet_Form(forms.ModelForm):
    class Meta:
        model = User_Wallet
        fields = "__all__"
        widgets = {
            'transaction_date': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class UserVehicle_Form(forms.ModelForm):
    class Meta:
        model = UserVehicle
        fields = "__all__"

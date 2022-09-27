from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Society(models.Model):
    CHOICE = {
        ("1", 'yes'),
        ("2", 'no')
    }
    name = models.CharField(max_length=30, blank=False)
    location = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=30, blank=False)
    state = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=30, default='India', error_messages={'required': 'Please enter your country'},
                               blank=False)
    two_wheel_hourly_price = models.FloatField(blank=False)
    two_wheel_weekly_price = models.FloatField(blank=False)
    two_wheel_monthly_price = models.FloatField(blank=False)
    two_wheel_daily_price = models.FloatField(blank=False)
    four_wheel_hourly_price = models.FloatField(blank=False)
    four_wheel_weekly_price = models.FloatField(blank=False)
    four_wheel_monthly_price = models.FloatField(blank=False)
    four_wheel_daily_price = models.FloatField(blank=False)
    number_of_parking = models.IntegerField(blank=False)
    opening_time = models.TimeField(blank=False)
    closing_time = models.TimeField(blank=False)
    longtitude = models.DecimalField(max_digits=10, decimal_places=8, blank=False)
    langtitude = models.DecimalField(max_digits=10, decimal_places=8, blank=False)
    bank_name = models.CharField(max_length=50, blank=False)
    branch = models.CharField(max_length=50, blank=False)
    account_number = models.BigIntegerField(blank=False, unique=True)
    ifsc_code = models.CharField(blank=False, max_length=50, unique=True)
    cancel_check = models.ImageField(upload_to='Society_Secretry/Docs/', blank=False)
    commision = models.FloatField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Society_Secretry(models.Model):
    society = models.OneToOneField(Society, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, default='', blank=False)
    address = models.CharField(max_length=100, default='', blank=False)
    city = models.CharField(max_length=30, default='', blank=False)
    country = models.CharField(max_length=30, default='', blank=False)
    state = models.CharField(max_length=30, default='', blank=False)
    mobile_number = PhoneNumberField(unique=True, default="+91", editable=True, blank=False)
    email = models.EmailField(unique=True, max_length=30, default='', blank=False)
    password = models.CharField(max_length=20, blank=False)
    aadhar_card = models.FileField(upload_to="Society_Secretry/Docs/", blank=False)
    aadhar_num = models.BigIntegerField(blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)



class Society_Commision_history(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    month = models.DateField(blank=True)
    payment_status = models.CharField(max_length=50, blank=True)
    amount = models.FloatField(blank=True)
    commision_paid_amount = models.FloatField(blank=True)
    commision_due_amount = models.FloatField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

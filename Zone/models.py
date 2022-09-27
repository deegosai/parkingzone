from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from User.models import User,UserVehicle
from Watchman.models import Watchman
from Society.models import Society
from django.utils.datetime_safe import datetime

# Create your models here.

class Park_slot(models.Model):
    CATEGORIES = {
        ("1", 'Free'),
        ("2", 'Booked'),
        ("3", 'Requested'),

    }

    society=models.ForeignKey(Society, on_delete=models.CASCADE)
    availability_status = models.CharField(max_length=255,default="1",choices=CATEGORIES,blank=True)
    has_owner = models.BooleanField(blank=True)
    is_reserved_slot=models.BooleanField(blank=True)
    slot_name  = models.CharField(max_length=255)
    latitude=models.DecimalField(max_digits=16, decimal_places=13,blank=True,null=True)
    langitude=models.DecimalField(max_digits=16, decimal_places=13,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.society.name+"-"+self.slot_name)

class Park_Slot_Owner(models.Model):
    park_slot = models.ForeignKey(Park_slot, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=False, error_messages={'required': 'Please enter your name'})
    address = models.CharField(max_length=50, blank=False, error_messages={'required': 'Please enter your address'})
    city = models.CharField(max_length=30, blank=False, error_messages={'required': 'Please enter your city'})
    mobile_number = PhoneNumberField(unique=True, default="+91", editable=True, blank=False)
    email = models.EmailField(unique=True,max_length=30, default='',blank=False)
    password = models.CharField(max_length=20,default='',blank=False)
    aadhar_card = models.FileField(upload_to="Building_Owner/Docs/", blank=False)
    aadhar_num = models.BigIntegerField(blank=False)
    bank_name = models.CharField(max_length=50, blank=False)
    branch = models.CharField(max_length=50, blank=False)
    account_number = models.BigIntegerField(blank=False, unique=True)
    ifsc_code = models.CharField(max_length=50,blank=False, unique=True)
    cancel_check = models.ImageField(upload_to='Building_Owner/Docs/', blank=False)
    commision = models.FloatField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)


class Park_Slot_Owner_Commision_history(models.Model):
    park_slot_owner = models.ForeignKey(Park_Slot_Owner, on_delete=models.CASCADE)
    month = models.DateField(blank=True)
    payment_status = models.CharField(max_length=50, blank=True)  ###Paid,not paid,xyz amount paid
    amount = models.FloatField(blank=True)
    commision_paid_amount = models.FloatField(blank=False)
    commision_due_amount = models.FloatField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.park_slot_owner.name)

class Zone_Booking(models.Model):
    PACKAGE = {
        ("Hourly", 'Hourly'),
        ("Daily", 'Daily'),
        ("Weekly", 'Weekly'),
        ("Monthly", 'Monthly')
    }

    BOOKING_STATUS = {
        ("Booked", 'Booked'),
        ("Requested", 'Requested'),
        ("Paid", 'Paid')
    }
    park_slot=models.ForeignKey(Park_slot,on_delete=models.CASCADE)
    vehicle=models.ForeignKey(UserVehicle,on_delete=models.CASCADE)
    booking_date=models.DateField(blank=True)
    activated_package_expire=models.DateField(blank=True)
    booking_arrival_time=models.TimeField(blank=True)
    booking_departure_time=models.TimeField(blank=True)
    activated_package=models.CharField(max_length=30, default='',blank=False,choices=PACKAGE)
    booking_amount=models.FloatField(default=0.0,blank=True)
    otp=models.IntegerField(null=True,blank=True)
    booking_status=models.CharField(max_length=30,blank=True,choices=BOOKING_STATUS)
    no_of_booking=models.IntegerField(default=0.0,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

class Zone_Booking_history(models.Model):
    PACKAGE = {
        ("Hourly", 'Hourly'),
        ("Daily", 'Daily'),
        ("Weekly", 'Weekly'),
        ("Monthly", 'Monthly')
    }

    BOOKING_STATUS = {
        ("Booked", 'Booked'),
        ("Requested", 'Requested'),
        ("Paid", 'Paid')
    }
    booking_id=models.IntegerField()
    checkin_date=models.DateField(blank=True)
    checkout_date = models.DateField(blank=True)
    checkin_time=models.TimeField(blank=True)
    checkout_time = models.TimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
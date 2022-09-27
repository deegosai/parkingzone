from django.db import models
from Society.models import *
from django.utils import timezone
# Create your models here.



class Admin(models.Model):
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=30)
    type=models.CharField(max_length=20,default="")
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.email

class Admin_Deal(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    commision = models.FloatField(blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)

class Admin_Wallet(models.Model):
    CATEGORIES = {
        ("1", 'Paid'),
        ("2", 'Due')
    }
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    month = models.DateField(blank=True,null=True)
    payment_status = models.CharField(max_length=50, blank=True,choices=CATEGORIES)
    amount = models.FloatField(blank=True)
    commision_paid_amount = models.FloatField(blank=True,default=0)
    commision_due_amount = models.FloatField(blank=True,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)


class Login(models.Model):
    number = models.IntegerField()
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=30)
    type=models.CharField(max_length=30, default="")
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)

class Notification(models.Model):
    message=models.CharField(max_length=150,blank=True)
    message_owner=models.CharField(max_length=100,blank=True)
    message_date=models.DateField(blank=True)
    message_time=models.TimeField(blank=True)
    is_read=models.BooleanField(default=False,blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)
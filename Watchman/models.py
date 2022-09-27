from django.db import models
from Society.models import Society
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Watchman(models.Model):
    society=models.ForeignKey(Society,on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=30, default='',blank=False)
    address=models.CharField(max_length=100, default='',blank=False)
    city=models.CharField(max_length=30, default='',blank=False)
    mobile_number=PhoneNumberField(unique=True,default="+91",editable=True,blank=False)
    email=models.EmailField(max_length=50,blank=False)
    password=models.CharField(max_length=20,default='',blank=False)
    aadhar_card=models.FileField(upload_to="Watchman/Documents",null=True,blank=False)
    aadhar_num=models.CharField(max_length=12,blank=False)
    passport_photo=models.ImageField(upload_to="WatchMan/Images",null=True,blank=True)
    salary=models.FloatField(blank=False)
    arrival_time=models.TimeField(blank=False)
    departure_time=models.TimeField(blank=False)
    join_date=models.DateTimeField( blank=False,auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)

class Watchman_payment(models.Model):
    watchman = models.ForeignKey(Watchman,on_delete=models.CASCADE)
    month = models.DateField(blank=True)
    payment_status = models.CharField(max_length=50, blank=True)
    salary = models.FloatField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
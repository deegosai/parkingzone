from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(models.Model):
    name = models.CharField(max_length=30, blank=False)
    country = models.CharField(max_length=30, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    mobile_number = PhoneNumberField(unique=True, default="+91", editable=True, blank=False)
    age = models.IntegerField(blank=True ,null=True)
    email = models.EmailField(max_length=50, blank=True)
    password = models.CharField(max_length=20, blank=True)
    confirm_password = models.CharField(max_length=20, blank=True)
    facebook_token = models.CharField(max_length=200, blank=True)
    google_token = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)


class UserVehicle(models.Model):
    V_TYPE = {
        ("1", '2 Wheeler'),
        ("2", '4 Wheeler'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=30, blank=True,choices=V_TYPE)
    vehicle_registration_no = models.CharField(blank=False, max_length=18)
    type_of_model = models.CharField(max_length=30, default='', blank=True)
    color = models.CharField(max_length=30, default='', blank=True)
    rc_book_no = models.CharField(max_length=30,blank=True)
    rc_book_front_file = models.ImageField(upload_to='User/VehicleDocs/', blank=True)
    rc_book_back_file = models.ImageField(upload_to='User/VehicleDocs/', blank=True)
    driving_lic_number = models.CharField(blank=True, max_length=15, default='')
    driving_lic_photo = models.ImageField(upload_to='User/VehicleDocs/', blank=True)
    refferal_user_num=models.IntegerField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name+"_"+self.type_of_model

class User_Activity(models.Model):
    TYPE = {
        ("Profile", 'Profile'),
        ("Booking", 'Booking'),
        ("Vehicle", 'Vehicle'),
        ("Wallet", 'Wallet'),
    }
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
    activity=models.CharField(max_length=300,blank=True)
    category=models.CharField(max_length=300,blank=True,choices=TYPE)
    act_date=models.DateField(blank=True,null=True)
    act_time=models.TimeField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)



class User_Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(blank=False, default=0.0)
    transaction_type = models.CharField(max_length=30, blank=True)
    transaction_amount = models.FloatField(default=0.0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)

class User_Transaction_history(models.Model):
    user_wallet = models.ForeignKey(User_Wallet, on_delete=models.CASCADE)
    balance = models.FloatField(blank=True, default=0.0,null=True)
    transaction_type = models.CharField(max_length=30, blank=True)
    transaction_amount = models.FloatField(default=0.0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)

class User_Wallet_bonus(models.Model):
    bonus = models.FloatField(blank=False, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True, blank=False)
    updated_at = models.DateTimeField(auto_now=True, blank=False)
    status = models.BooleanField(default=False)
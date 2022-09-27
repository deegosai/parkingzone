from django.contrib import admin
from .models import Admin,Login,Admin_Wallet,Admin_Deal,Notification
# Register your models here.
admin.site.register(Admin)
admin.site.register(Login)
admin.site.register(Admin_Wallet)
admin.site.register(Admin_Deal)
admin.site.register(Notification)

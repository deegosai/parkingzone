from django.contrib import admin
from .models import *
# Register your models here.
class User_Admin(admin.ModelAdmin):
    list_display = ('id','name', 'created_at', 'updated_at')
class User_Wallet_Admin(admin.ModelAdmin):
    list_display = ('id', 'user_name','created_at', 'updated_at')
    def user_name(self, instance):
        return instance.user.name

class UserVehicle_Admin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'created_at', 'updated_at')
    def user_name(self, instance):
        return instance.user.name

class User_Transaction_history_Admin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'created_at', 'updated_at')

    def user_name(self, instance):
        return instance.user_wallet.user.name


class User_Activity_Admin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'created_at', 'updated_at')

    def user_name(self, instance):
        return instance.user.name

admin.site.register(User,User_Admin)
admin.site.register(User_Wallet,User_Wallet_Admin)
admin.site.register(UserVehicle,UserVehicle_Admin)
admin.site.register(User_Transaction_history,User_Transaction_history_Admin)
admin.site.register(User_Wallet_bonus)
admin.site.register(User_Activity,User_Activity_Admin)

# admin.py


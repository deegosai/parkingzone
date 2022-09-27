from django.contrib import admin
from .models import Watchman,Watchman_payment
# Register your models here.
class Watchman_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')


class Watchman_payment_Admin(admin.ModelAdmin):
    list_display = ('id', 'watchman_name', 'created_at', 'updated_at')

    def watchman_name(self, instance):
        return instance.watchman.name


admin.site.register(Watchman,Watchman_Admin)
admin.site.register(Watchman_payment,Watchman_payment_Admin)

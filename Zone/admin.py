from django.contrib import admin
from .models import *

# Register your models here.
class Park_slot_Admin(admin.ModelAdmin):
    list_display = ('id', 'slot_name','soc_name', 'created_at', 'updated_at')

    def soc_name(self, instance):
        return instance.society.name

class Park_Slot_Owner_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')

class Park_Slot_Owner_Commision_history_Admin(admin.ModelAdmin):
    list_display = ('id', 'po_name', 'created_at', 'updated_at')

    def po_name(self, instance):
        return instance.park_slot_owner.name

class Zone_Booking_Admin(admin.ModelAdmin):
    list_display = ('id', 'user_name', 'soc_name','created_at', 'updated_at')

    def user_name(self, instance):
        return instance.vehicle.user.name

    def soc_name(self, instance):
        return instance.park_slot.society.name

admin.site.register(Park_slot,Park_slot_Admin)
admin.site.register(Park_Slot_Owner,Park_Slot_Owner_Admin)
admin.site.register(Park_Slot_Owner_Commision_history,Park_Slot_Owner_Commision_history_Admin)
admin.site.register(Zone_Booking,Zone_Booking_Admin)


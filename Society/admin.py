from django.contrib import admin
from.models import Society,Society_Secretry,Society_Commision_history
# Register your models here.
class Society_Admin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')

class Society_Secretry_Admin(admin.ModelAdmin):
    list_display = ('id', 'name','soc_name', 'created_at', 'updated_at')

    def soc_name(self, instance):
        return instance.society.name

class Society_Commision_history_Admin(admin.ModelAdmin):
    list_display = ('id', 'soc_name', 'created_at', 'updated_at')

    def soc_name(self, instance):
        return instance.society.name

admin.site.register(Society,Society_Admin)
admin.site.register(Society_Secretry,Society_Secretry_Admin)
admin.site.register(Society_Commision_history,Society_Commision_history_Admin)

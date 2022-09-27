from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [

                  path('Admin_Create/', Admin_Create, name="Admin_create"),
                  path('adminlogin/', adminlogin, name='adminlogin'),
                  path('logout/', logout, name='logout'),
                  path('dashboard/', dashboard, name='dashboard'),
                  path('society_make_payment/', society_and_admin_payment_report,
                       name="society_and_admin_payment_report"),
                  path('society_save_payment/', save_soc_Payment, name="save_soc_Payment"),
                  path('update_soc_Payment/', update_soc_Payment, name="update_soc_Payment"),
                  path('save_ps_owner_Payment/', save_ps_owner_Payment, name="save_ps_owner_Payment"),
                  path('parkzone_notify/', parkzone_notify, name="parkzone_notify"),
                  path('parkzone_notify_change/', parkzone_notify_change, name="parkzone_notify_change"),
                  path('notifaction_detail/', notifaction_detail, name="notifaction_detail"),
                  path('update_park_slot_owner_Payment/', update_park_slot_owner_Payment, name="update_park_slot_owner_Payment"),
                  path('society_payment_record/', society_payment_record, name="society_payment_record"),
                  path('parkingslotowner_and_admin_payment_report/', parkingslotowner_and_admin_payment_report,
                       name="parkingslotowner_and_admin_payment_report"),
                  path('parkslot_owner_payment_record/', parkslot_owner_payment_record,
                       name="parkslot_owner_payment_record"),


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('Zone/Detail/', views.zone_detail_view, name="zone_detail_view"),
                  path('Zones/View/', views.ZonesView, name="ZonesView"),
                  path('Zone/Register/', views.ZoneRegister, name="ZoneRegister"),
                  path('Zone/Update/', views.ZoneUpdate, name="ZoneUpdate"),
                  path('Zone/Delete/', views.ZoneDelete, name="ZoneDelete"),
                  path('User/otp_verify/', views.user_otp_verify, name="user_otp_verify"),
                  path('Zone/checkout/', views.user_checkout, name="user_checkout"),
                  path('Zone/ServicePackage_detail/', views.servicePackage_detail, name="servicePackage_detail"),
                  path('Zone/bookingFreeTimes/', views.giveFreeTime_Booking, name="giveFreeTime_Booking"),
                  path('Zone/Reservedslots/', views.reserved_slots_list, name="reserved_slots_list"),

                  path('Booking/History/', views.BookingHistory, name="BookingHistory"),
                  path('Booking/Register/', views.BookingRegister, name="BookingRegister"),
                  path('Booking/Acknowlege/', views.user_booking_acknowlegde_msg, name="user_booking_acknowlegde_msg"),
                  path('Booking/Update/', views.BookingUpdate, name="BookingUpdate"),
                  path('Booking/Cancel/', views.Booking_Cancel, name="Booking_Cancel"),
                  path('Booking/Detail/', views.booking_detail_view, name="booking_detail_view"),

                  path('Zone_view/', views.Zone_view, name="Zone_view"),
                  path('Zone_create/', views.Zone_create, name="Zone_create"),
                  path('Zone_edit/', views.Zone_edit, name="Zone_edit"),
                  path('Zone_update/', views.Zone_update, name="Zone_update"),
                  path('Zone_delete/', views.Zone_delete, name="Zone_delete"),
                  path('Booking_view/', views.Booking_view, name="Booking_view"),
                  path('Booking_history/', views.show_booking_history, name="show_booking_history"),

                  path('parkslot_owner_view_form/', views.parkslot_owner_view_form, name="parkslot_owner_view_form"),
                  path('parkslot_owner_create_form/', views.parkslot_owner_create_form,
                       name="parkslot_owner_create_form"),
                  path('parkslot_owner_delete_form/', views.parkslot_owner_delete_form,
                       name="parkslot_owner_delete_form"),
                  path('parkslot_owner_edit_form/', views.parkslot_owner_edit_form, name="parkslot_owner_edit_form"),
                  path('parkslot_owner_update_form/', views.parkslot_owner_update_form,
                       name="parkslot_owner_update_form"),
                  path('pz_society_detail_view/', views.pz_society_detail_view, name="pz_society_detail_view"),
                  path('parkzone_user_view/', views.parkzone_user_view,
                       name='parkzone_user_view'),
                  path('Zone_popupview/', views.Zone_popupview, name="Zone_popupview"),
                  path('parkzone_park_slot_detail_view/', views.parkzone_park_slot_detail_view,
                       name='parkzone_park_slot_detail_view'),
                  path('parkzone_park_slot_owner_detail_edit/', views.parkzone_park_slot_owner_detail_edit,
                       name='parkzone_park_slot_owner_detail_edit'),
                  path('parkzone_park_slot_owner_detail_update/', views.parkzone_park_slot_owner_detail_update,
                       name='parkzone_park_slot_owner_detail_update'),
                  path('parkzone_park_slot_owner_detail_view/', views.parkzone_park_slot_owner_detail_view,
                       name='parkzone_park_slot_owner_detail_view'),
                  path('owner_view1/', views.owner_view1,
                       name='owner_view1'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

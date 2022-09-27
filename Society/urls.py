from django.urls import path

from .views import *
urlpatterns = [
    path('Society/Create/', society_Create, name="soc_create"),
    path('Societies/Search/', search_societies, name="search_societies"),
    path('Society/Update/', society_Update, name="soc_update"),
    path('Society/Delete/', society_Delete, name="soc_delete"),
    path('Society/Detail/', society_detail_view, name="soc_detail"),

    path('Societysecretry/register/', SocietysecretryRegister, name="SocietysecretryRegister"),
    path('Societysecretry/update/', SocietysecretryUpdate, name="SocietysecretryUpdate"),
    path('Societysecretry/delete/', SocietysecretryDelete, name="SocietysecretryDelete"),

    #############__________admin_panel_________##############################
    path('Society_view/', pz_society_view, name="pz_society_view"),
    path('Society_edit/', pz_society_edit, name="pz_society_edit"),
    path('Society_create/', pz_society_create, name="pz_society_create"),
    path('Society_update/', pz_society_update, name="pz_society_update"),
    path('Society_delete/', pz_society_delete, name="pz_society_delete"),

    path('Societysecretry_create/', Societysecretry_create, name="Societysecretry_create"),
    path('Societysecretry_view/', Societysecretry_view, name="Societysecretry_view"),
    path('Societysecretry_edit/', Societysecretry_edit, name="Societysecretry_edit"),
    path('Societysecretry_update/', Societysecretry_update, name="Societysecretry_update"),
    path('Societysecretry_delete/', Societysecretry_delete, name="Societysecretry_delete"),

    path('pz_society_detail/', pz_society_detail, name="pz_society_detail"),
    path('pz_society_detail_edit/', pz_society_detail_edit, name="pz_society_detail_edit"),
    path('pz_society_detail_update/', pz_society_detail_update, name="pz_society_detail_update"),

    path('pz_society_billing/', pz_society_billing, name="pz_society_billing"),
    path('pz_parking_owner_billing/', pz_parking_owner_billing, name="pz_parking_owner_billing"),
    path('some_view/', some_view, name="some_view"),
    path('society_report/', society_report, name="society_report"),
    path('watchaman_records/', watchaman_records, name="watchaman_records"),
    path('park_slot_detail/', park_slot_detail, name="park_slot_detail"),
    path('park_slot_detail_edit/', park_slot_detail_edit, name="park_slot_detail_edit"),
    path('park_slot_detail_update/', park_slot_detail_update, name="park_slot_detail_update"),

    path('watchaman_records/', watchaman_records, name="watchaman_records"),
    path('user_record/', user_record, name="user_record"),
    path('zone_record/', zone_record, name="zone_record"),
    path('Societysecretry_profile_view/', Societysecretry_profile_view, name="Societysecretry_profile_view"),
    path('Societysecretry_Profile_edit/', Societysecretry_Profile_edit, name="Societysecretry_Profile_edit"),
    path('Societysecretry_profile_update/', Societysecretry_profile_update, name="Societysecretry_profile_update"),
    path('park_slot_detail_create/', park_slot_detail_create, name="park_slot_detail_create"),
    path('society_view1/', society_view1, name="society_view1"),
    path('societyowner_view1/', societyowner_view1, name="societyowner_view1"),
]

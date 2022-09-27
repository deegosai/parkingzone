from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
                  path('watchman/view/', views.WatchmanView, name="WatchmanView"),
                  path('Watchman/Register/', views.WatchmanRegister, name="WatchmanRegister"),
                  path('Watchman/Edit_Profile/', views.WatchmanUpdate, name="WatchmanUpdate"),
                  path('watchman/delete/', views.WatchmanDelete, name="WatchmanDelete"),
                  path('watchman/detail/', views.watchman_detail_view, name="Watchman_detail"),
                  path('Watchman/Login/', views.watchman_Login, name="WatchmanLogin"),
                  path('Watchman/Society_details/', views.watchman_Society_details, name="watchman_Society_details"),
                  path('Watchman/zone_status/', views.zone_status, name="zone_status"),
                  path('Watchman/zone_booked/', views.zone_booked, name="zone_booked"),
                  path('Watchman/Vehicle_transfer/', views.transfer_vehicle, name="transfer_vehicle"),
path('Watchman/SaveSlotMarks/', views.saveSlotMarks, name="saveSlotMarks"),

                  path('watchman_create/', views.watchman_create, name="watchman_create"),
                  path('watchman_view/', views.watchman_view, name="watchman_view"),
                  path('watchman_edit/', views.watchman_edit, name="watchman_edit"),
                  path('watchman_update/', views.watchman_update, name="watchman_update"),
                  path('watchman_delete/', views.watchman_delete, name="watchman_delete"),


                  path('watchman_payment_record/', views.watchman_payment_record, name="watchman_payment_record"),
                  path('watchman_salary_payment_record/', views.watchman_salary_payment_record,
                       name="watchman_salary_payment_record"),
                  path('watchman_salary_final_payment/', views.watchman_salary_final_payment,
                       name="watchman_salary_final_payment"),
                  path('watchman_salary_history_records/', views.watchman_salary_history_records,
                       name="watchman_salary_history_records"),
                  path('warchman_view1/', views.warchman_view1, name="warchman_view1"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

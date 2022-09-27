from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

# otpmsg="http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=<str:pk>&message=<str:pk>"
# booking_otp="http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=<str:pk>&message="
urlpatterns = [
                  path('User/Register/', user_register, name="user_register"),
                  path('User/Login/', user_Login, name='UserLogin'),
                  path('User/SocialRegister/', user_social_Register, name='user_social_Register'),
                  path('User/SocialLogin/', user_social_Login, name='user_social_Login'),
                  path('User/Edit_Profile/', user_edit_profile, name="user_edit_profile"),
                  path('User/ProfileView/', user_detail_view, name="user_detail_view"),
                  path('User/Register_otp/', registerOTP, name="registerOTP"),
                  path('User/forgot_password/', user_forgot_password, name="forgot_password"),
                  path('User/Status/', user_status_change, name="user_status_change"),

                  path('User/ChangePassword/', user_change_password, name="user_change_password"),
                  path('UserWallet/AddMoney/', user_wallet_add_money, name="uw_add_money"),
                  path('UserWallet/CutMoney/', user_wallet_cut_money, name="uw_cut_money"),
                  path('UserWallet/Detail/', userwallet_detail_view, name="uw_detail"),
                  path('UserWallet/transaction_history/', userwallet_transaction_history,
                       name="userwallet_transaction_history"),

                  path('Vehicle/View/', vehicle_details_view, name="v_view"),
                  path('Vehicles/View/', vehicles_view, name="vs_view"),
                  path('Vehicle/Update/', vehicle_details_update, name="v_update"),
                  path('Vehicle/Add/', vehicle_details_added, name="v_create"),
                  path('Vehicle/Delete/', vehicle_Delete, name="v_delete"),
                  path('Refferal_Vehicle/Add/', refferal_vehicle_details_add, name="refferal_vehicle_details_add"),
                  path('Refferal_Vehicle/msg_confirm/', refferal_vehicle_msg, name="refferal_vehicle_msg"),

                  path('Vehicle_owner_vehicle/display/', vehicle_owner_vehicle_display,
                       name="vehicle_owner_vehicle_display"),
                  path('Refferal_user_vehicle/display/', refferal_user_vehicle_display,
                       name="refferal_user_vehicle_display"),

                  path('User_view/', pz_user_view, name="pz_user_view"),
                  path('User_create/', pz_user_create, name="pz_user_create"),
                  path('User_edit/', pz_user_edit, name="pz_user_edit"),
                  path('User_update/', pz_user_update, name="pz_user_update"),

                  path('user_activity/', user_activity, name="user_activity"),

                  path('userwallet_create_form/', userwallet_create_form, name="userwallet_create_form"),
                  path('userwallet_view_form/', userwallet_view_form, name="userwallet_view_form"),
                  path('userwallet_form_edit/', userwallet_form_edit, name="userwallet_form_edit"),
                  path('userwallet_update_form/', userwallet_update_form, name="userwallet_update_form"),
                  path('userwallet_delete_form/', userwallet_delete_form, name="userwallet_delete_form"),
                  path('userwallet_add_bonus_money/', userWallet_bonus_add, name="userWallet_bonus_add"),

                  path('UserVehicle_view/', pz_uservehicle_view, name="pz_uservehicle_view"),
                  path('UserVehicle_create/', pz_uservehicle_create, name="pz_uservehicle_create"),
                  path('UserVehicle_edit/', pz_uservehicle_edit, name="pz_uservehicle_edit"),
                  path('UserVehicle_update/', pz_uservehicle_update, name="pz_uservehicle_update"),
                  path('UserVehicle_delete/', pz_uservehicle_delete, name="pz_uservehicle_delete"),
                  path('user_view1/', user_view1, name="user_view1"),
                  path('vehicle_view1/', vehicle_view1, name="vehicle_view1"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

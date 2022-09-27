import os

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import date, datetime
from Watchman.middlewares import Parkzone_middleware
from . import User_Panel_Validations
from .User_API_Validation import *
from .forms import User_Form, User_Wallet_Form, UserVehicle_Form
from .models import *
import json
from .models import User
import random
from .serializers import *
from os import system
from ParkZone.settings import DOMAIN, PORT
from django.http import HttpResponse

path1 = 'http://' + DOMAIN + ':' + PORT + '/media/'


##########Create your views here.
@api_view(['POST'])
def user_register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        validationMessage = userAPI_Validations(request, User, "create")
        if validationMessage == True:
            # otp(mob, 1234)
            if serializer.is_valid():
                abc = serializer.save()
                print(abc)
                bonus=User_Wallet_bonus.objects.all()
                if bonus:
                    walletdata = {'user': abc.id, 'balance': bonus[0].bonus}
                else:
                    walletdata = {'user': abc.id, 'balance': 0.0}
                serializerWallet = UserWalletSeriallizer(data=walletdata)
                serializerWallet = UserWalletSeriallizer(data=walletdata)
                if serializerWallet.is_valid():
                    walletObj=serializerWallet.save()

                    data = serializer.data
                    print("data---",data)
                    activity1=data['name']+" registered in ParkZone"
                    activity2=walletObj.user.name + "'s wallet created with balance "+str(walletObj.balance)
                    userAct1=User_Activity(user=abc,activity=activity1,category="Profile",)

                    userAct1.save()
                    userAct2 = User_Activity(user=abc,activity=activity2,category="Profile")
                    userAct2.save()
                    return Response({"error": "0", "message": "User created succesfully", "data": data, })
                else:
                    print(serializerWallet.errors)
                    return Response({"error": "1", "message": "Can't create wallet", "data": []})

            else:
                return Response({"error": "13", "message": list(serializer.errors.values())[0][0], "data": []})
        else:
            varray = validationMessage.split(":")
            return Response({"error": varray[0], "message": varray[1], "data": []})

@api_view(['POST'])
def registerOTP(request):
    mob1 = request.POST["mobile_number"]
    otp = request.POST["otp"]

    dict = {}

    otp_msg = "http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=" + str(
        mob1) + "&message=" + "Your OTP for Parkzone registration is "+str(otp)
    dict["register_otp"] = otp_msg

    return Response({"error": "0", "message": "User details found", "data": dict})

@api_view(['POST'])
def user_Login(request):
    if request.method == "POST":
        mobilenumber = request.POST['mobile_number']
        password = request.POST['password']
        if not (mobilenumber and password):
            return Response({"error": "2", "message": "Your Mobile Number Or Password Is Blank", "data": []})
        else:
            if User.objects.filter(mobile_number=mobilenumber, password=password,status=True).exists():
                data = User.objects.filter(mobile_number=mobilenumber, password=password).values()

                data1 = list(data)
                userwallet = User_Wallet.objects.get(user=data[0]['id'])

                dict = {}
                dict['wallet_id'] = userwallet.id
                data1[0]['wallet_id'] = userwallet.id

                return Response({"error": "0", "message": "You Are Now Login Successfully", "data": data1})
            else:
                return Response({"error": "1", "message": "Your User_name or Password Is Incorrect", "data": []})


@api_view(['POST'])
def user_forgot_password(request):
    mob1 = request.POST["mobile_number"]
    otp = request.POST["otp"]
    print("----1---------", mob1)
    dict = {}
    if User.objects.filter(mobile_number=mob1).exists():
        user=User.objects.get(mobile_number=mob1)
        otp_msg = "http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=" + str(
            mob1) + "&message=" + "Use this OTP "+str(otp)+ " to reset your password with Parkzone"
        dict["forgot_password_otp"] = otp_msg
        dict["user_id"]=user.id
        dict["user_name"]=user.name

        return Response({"error": "0", "message": "User details found", "data": dict})
    else:
        return Response({"error": "1", "message": "User not exists", "data": []})



@api_view(['POST'])
def user_change_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        userid = request.POST['user_id']
        if User.objects.filter(id=userid).exists():
            user = User.objects.get(id=userid)
            user.password = password
            user.confirm_password = confirm_password
            user.save()
            serializer = UserSerializer(instance=user)
            activity=user.name+" changed password "
            activityObj=User_Activity(user=user,activity=activity,category="Profile")
            activityObj.save()

            return Response({"error": "0", "data": serializer.data, "message": "Password changed successfully"})
        else:
            return Response({"error": "1", "data": [], "message": "User already exist."})


@api_view(['POST'])
def user_social_Register(request):
    mobile_number = request.POST['mobile_number']
    token = request.POST['token']
    type = request.POST['type']
    name = request.POST['name']

    account = User()
    print("############  1 ###########################")
    if type == "Google":
        print("############  google ###########################")
        email = request.POST['email']
        if User.objects.filter(google_token=token).exists():
            return Response({"error": "1", "data": [], "message": "This token already exist."})
        elif User.objects.filter(email=email).exists():
            return Response({"error": "2", "data": [], "message": "This email already exist."})
        else:
            print(email)
            account.email = email
            account.google_token = token

    elif type == "Facebook":
        print("############  fb ###########################")
        if User.objects.filter(facebook_token=token).exists():
            return Response({"error": "2", "data": [], "message": "This token already exist."})
        else:
            account.facebook_token = token

    if User.objects.filter(mobile_number=mobile_number).exists():
        return Response({"error": "3", "data": [], "message": "This mobile number is already registered"})
    else:
        print(mobile_number)
        account.mobile_number = mobile_number


    account.name = name
    account.save()
    serializer = UserSerializer(instance=account)
    bonus = User_Wallet_bonus.objects.all()
    if bonus:
        wallet = User_Wallet.objects.create(user=account, balance=bonus[0].bonus)
        wallet.save()
    else:
        wallet = User_Wallet.objects.create(user=account, balance=0.0)
        wallet.save()
    activity1 = account.name + " registered in ParkZone"
    activity2 = account.name + "'s wallet created with balance " + str(wallet.balance)

    userAct1 = User_Activity(user=account, activity=activity1,category="Profile")
    userAct1.save()
    userAct2 = User_Activity(user=account, activity=activity2,category="Profile")
    userAct2.save()
    return Response({"error": "0", "message": "User Registered succsesfully", "data": serializer.data, })



@api_view(['POST'])
def user_social_Login(request):
    if request.method == "POST":

        token = request.POST['token']
        type = request.POST['type']
        if not (token):
            return Response({"error": "2", "message": "Something went wrong !!", "data": []})
        else:
            if type == "Google":
                if User.objects.filter(google_token=token).exists():
                    data = User.objects.filter(google_token=token).values()
                    print(data)
                    data1 = list(data)
                    userwallet = User_Wallet.objects.get(user=data[0]['id'])

                    dict = {}
                    dict['wallet_id'] = userwallet.id
                    data1[0]['wallet_id'] = userwallet.id

                    return Response({"error": "0", "message": "You Are Now Login Successfully", "data": data1})
                else:
                    return Response({"error": "1", "message": "Something went wrong !!", "data": []})
            elif type == "Facebook":
                if User.objects.filter(facebook_token=token).exists():
                    data = User.objects.filter(facebook_token=token).values()
                    data1 = list(data)
                    userwallet = User_Wallet.objects.get(user=data[0]['id'])
                    dict = {}
                    dict['wallet_id'] = userwallet.id
                    data1[0]['wallet_id'] = userwallet.id
                    return Response({"error": "0", "message": "You Are Now Login Successfully", "data": data1})
                else:
                    return Response(
                        {"error": "1", "message": "Something went wrong !!", "data": []})


@api_view(['POST'])
def user_edit_profile(request):
    pk = request.POST['id']
    isUser = User.objects.filter(id=pk).exists()
    if isUser:
        user = User.objects.get(id=pk)
        print(request.data, "-----------")
        serializer = UserEditSerializer(instance=user, data=request.data)

        validationMessage = userAPI_Validations(request, User, "update")
        if validationMessage == True:
            if serializer.is_valid():
                serializer.save()

                activity = serializer.data['name'] + " edited profile "
                activityObj = User_Activity(user=user,activity=activity,category="Profile")
                activityObj.save()
                return Response(
                    {"error": "0", "message": "User profile updated successfully", "data": serializer.data})
            else:
                return Response(
                    {"error": "4", "message": "User profile not updated, something went wrong", "data": []})
        else:
            print("in else :::", validationMessage)
            varray = validationMessage.split(":")
            return Response({"error": varray[0], "message": varray[1], "data": []})
    else:
        return Response({"error": "5", "message": "User not found", "data": []})


# @api_view(['POST', 'DELETE'])
# def user_Delete(request):
#     pk = request.POST['id']
#     user = User.objects.get(id=pk)
#     if user:
#         user.delete()
#         return Response({"error": "0", "message ": "Data Deleted"})
#     else:
#         return Response({"error": "1", "message": "Data not deleted"})


@api_view(['POST'])
def user_detail_view(request):
    pk = request.POST['id']
    isUser = User.objects.filter(id=pk).exists()
    if isUser:
        user = User.objects.filter(id=pk).values()
        return Response({"error": "0", "message": "User detail found", "data": user, })
    else:
        return Response({"error": "1", "message": "User not found", "data": []})

@api_view(['POST'])
def user_status_change(request):
    status = request.POST['user_status']
    userid=request.POST['userid']
    isUser = User.objects.filter(id=userid).exists()
    if isUser:
        user = User.objects.get(id=userid)
        user.status=True
        user.save()
        # serializer=UserSerializer(instance=user)
        return Response({"error": "0", "message": "Register successfull", "data": [], })
    else:
        return Response({"error": "1", "message": "User not found", "data": []})
# #####################################User_Wallet###########################################
#
# @api_view(['POST'])
# def user_wallet_Create(request):
#     if request.method == 'POST':
#         serializer = UserWalletSeriallizer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"error": "0", "message ": "Data created succesfully", "data": serializer.data, })
#         else:
#             return Response({"error": "1", "message": "Can't create data"})


@api_view(['POST'])
def user_wallet_add_money(request):
    getuser = request.POST['user']
    isUser = User.objects.filter(id=getuser).exists()
    if isUser:
        pk = request.POST['wallet_id']
        isWallet = User_Wallet.objects.filter(id=pk).exists()
        if isWallet:
            amount = request.POST['transaction_amount']
            if amount == "" or amount == None:
                return Response({"error": "3", "message": "Enter valid amount", "data": []})
            else:
                user_wallet = User_Wallet.objects.get(id=pk)
                balance = float(user_wallet.balance) + float(amount)
                user_wallet.transaction_amount = float(amount)
                user_wallet.balance = balance
                user_wallet.save()
                serializer = UserWalletSeriallizer(instance=user_wallet)
                transaction = User_Transaction_history.objects.create(user_wallet=user_wallet)
                transaction.transaction_type = "Credit"
                transaction.balance=user_wallet.balance
                transaction.transaction_amount = float(amount)
                transaction.save()

                activity = user_wallet.user.name + " has "+transaction.transaction_type+"ed "+str(transaction.transaction_amount)+". so, balance is "+str(user_wallet.balance)
                activityObj = User_Activity(user=user_wallet.user,activity=activity,category="Wallet")
                activityObj.save()

                return Response({"error": "0", "message": "Money added to wallet", "data": serializer.data, })
        else:
            return Response({"error": "2", "message": "Wallet not exists", "data": []})
    else:
        return Response({"error": "1", "message": "User not exists", "data": []})


@api_view(['POST'])
def user_wallet_cut_money(request):
    getuser = request.POST['user']
    isUser = User.objects.filter(id=getuser).exists()
    if isUser:
        pk = request.POST['wallet_id']
        isWallet = User_Wallet.objects.filter(id=pk).exists()
        if isWallet:
            amount = request.POST['transaction_amount']
            if amount == "" or amount == None:
                return Response({"error": "3", "message": "Enter valid amount", "data": []})
            else:
                user_wallet = User_Wallet.objects.get(id=pk)
                balance = float(user_wallet.balance) - float(amount)
                user_wallet.transaction_amount = float(amount)
                user_wallet.balance = balance
                user_wallet.save()
                serializer = UserWalletSeriallizer(instance=user_wallet)
                transaction = User_Transaction_history.objects.create(user_wallet=user_wallet)
                transaction.transaction_type = "Debit"
                transaction.balance = user_wallet.balance
                transaction.transaction_amount = float(amount)
                transaction.save()

                activity = user_wallet.user.name + " has " + transaction.transaction_type + "ed " + str(
                    transaction.transaction_amount) + ". so, balance is " + str(user_wallet.balance)
                activityObj = User_Activity(user=user_wallet.user,activity=activity,category="Wallet")
                activityObj.save()

                serializer = UserTransactionSeriallizer(instance=transaction)
                return Response({"error": "0", "message": "Money debited from wallet", "data": serializer.data, })

        else:
            return Response({"error": "2", "message": "Wallet not exists", "data": []})
    else:
        return Response({"error": "1", "message": "User not exists", "data": []})


@api_view(['POST'])
def userwallet_detail_view(request):
    pk = request.POST['userid']
    isuser = User.objects.filter(id=pk).exists()
    if isuser:
        userobj = User.objects.get(id=pk)
        user_wallet = User_Wallet.objects.get(user=userobj)
        dict = {}
        dict['balance'] = user_wallet.balance
        dict['wallet_id'] = user_wallet.id
        if user_wallet:
            return Response({"error": "0", "message": "User Wallet balance found", "data": dict, })
        else:
            return Response({"error": "1", "message": "User Wallet balance not found", "data": []})
    else:
        return Response({"error": "2", "message": "User not exists", "data": []})


@api_view(['POST'])
def userwallet_transaction_history(request):
    userid = request.POST['userid']
    isuser = User.objects.filter(id=userid).exists()
    if isuser:
        user = User.objects.get(id=userid)
        wallet = User_Wallet.objects.get(user=user.id)
        print("wallet---", wallet)
        tasks = User_Transaction_history.objects.filter(user_wallet=wallet.id).values()
        print("tasks--", tasks)
        # serializer = UserTransactionSeriallizer(instance=tasks)

        return Response({"error": "0", "message": "Transaction history found", "data": tasks, })
        # else:
        #     return Response({"error": "1", "message": "Transaction history not found"})
    else:
        return Response({"error": "2", "message": "User not exists", "data": []})


# #############################################_____vehicle_api_______######################################
@api_view(['POST'])
def vehicles_view(request):
    pk = request.POST['user']

    vehicles = UserVehicle.objects.filter(user=pk).values() | UserVehicle.objects.filter(refferal_user_num=pk).values()
    print("------vehicles------",vehicles)
    # vehicles_owner = UserVehicle.objects.filter(refferal_user_num=pk).values()
    # print("------vehicles_owner-------", vehicles_owner)
    if vehicles or list(vehicles)!=[]:
        data = list(vehicles)
        for x in data:
            print(x)
            x['rc_book_back_file'] = path1 + "" + x['rc_book_back_file']
            x['driving_lic_photo'] = path1 + "" + x['driving_lic_photo']
            x['rc_book_front_file'] = path1 + "" + x['rc_book_front_file']
            if x['refferal_user_num'] == None:
                userObj = User.objects.get(id=x['user_id'])
                x['username'] = userObj.name
                x['user_num'] = str(userObj.mobile_number)
                x['owner_name'] = userObj.name
                x['owner_num'] = str(userObj.mobile_number)
            else:
                userObj = User.objects.get(id=x['user_id'])
                refferalObj = User.objects.get(id=x['refferal_user_num'])
                x['username'] =userObj.name
                x['user_num'] = str(userObj.mobile_number)
                x['owner_name'] = refferalObj.name
                x['owner_num'] = str(refferalObj.mobile_number)

        return Response({"error": "0", "message": "Vehicle detail visible", "data": data, })

    else:
        return Response({"error": "1", "message": "Vehicle detail not visible", "data": []})


@api_view(['POST'])
def vehicle_details_view(request):
    pk = request.POST['vehicle_id']
    vehicle = UserVehicle.objects.filter(id=pk).exists()
    if vehicle:
        vehicle = UserVehicle.objects.filter(id=pk).values()
        data = list(vehicle)
        data[0]['rc_book_back_file'] = path1 + "" + data[0]['rc_book_back_file']
        data[0]['driving_lic_photo'] = path1 + "" + data[0]['driving_lic_photo']
        data[0]['rc_book_front_file'] = path1 + "" + data[0]['rc_book_front_file']
        if vehicle:
            return Response({"error": "0", "message": "Vehicle detail visible", "data": vehicle})
        else:
            return Response({"error": "1", "message": "Vehicle detail not visible", "data": []})
    else:
        return Response({"error": "2", "message": "Vehicle not exists", "data": []})


@api_view(['POST'])
def vehicle_details_added(request):
    print("Vehicle Added :::::")
    serializer = VehicleSerializer(data=request.data)
    print(serializer)
    pk = request.POST['user']
    print(pk)

    isuser = User.objects.filter(id=pk).exists()
    print(isuser)

    if isuser:
        validationMessage = userVehicle_API_Validations(request, UserVehicle, "create")
        print("Validation Msg" , validationMessage)
        if validationMessage == True:
            if serializer.is_valid():
                print("serializer Error in ")
                serializer.save()
                print("serializer Error in 2")

                print("serializer-----", serializer.data)
                user=User.objects.get(id=pk)
                if serializer.data['type']=="1":
                    type="two wheeler"
                else:
                    type="four wheeler"
                activity = user.name + " added " + type + " vehicle of registration number "\
                           + serializer.data['vehicle_registration_no']
                activityObj = User_Activity(user=user,activity=activity,category="Vehicle")
                activityObj.save()
                print("##################################", serializer.data)
                return Response(
                    {"error": "0", "message": "Vehicle details added succesfully", "data": serializer.data})
            else:
                print("serializer Error",serializer.errors)
                return Response({"error": "1", "message": list(serializer.errors.values())[0][0], "data": []})
        else:
            varray = validationMessage.split(":")
            print(varray)
            return Response({"error": varray[0], "message": varray[1], "data": []})
    else:
        return Response({"error": "2", "message": "User not exists", "data": []})


@api_view(['POST'])
def vehicle_details_update(request):
    user_id = request.POST['user']
    vehicle_id = request.POST['vehicle_id']
    isUser = User.objects.filter(id=user_id).exists()
    if isUser:
        userObj = User.objects.get(id=user_id)
        is_uservehicle = UserVehicle.objects.filter(user=userObj, id=vehicle_id).exists()
        if is_uservehicle:
            vehicle = UserVehicle.objects.get(user=userObj, id=vehicle_id)
            if vehicle.refferal_user_num == None:
                serializer = VehicleSerializer(instance=vehicle, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    activity = userObj.name + " updated  vehicle of registration number " \
                               + serializer.data['vehicle_registration_no']
                    activityObj = User_Activity(user=userObj, activity=activity, category="Vehicle")
                    activityObj.save()
                    return Response({"error": "0", "message": "Vehicle details Updated", "data": serializer.data, })
                else:
                    return Response({"error": "4", "message": list(serializer.errors.values())[0][0], "data": []})
            else:
                return Response(
                    {"error": "3", "message": str(userObj.name) + " can not update this vehicle", "data": []})
        else:
            return Response({"error": "2", "message": "Vehicle not found", "data": []})
    else:
        return Response({"error": "1", "message": "User not found", "data": []})


@api_view(['POST'])
def vehicle_Delete(request):
    vehicle_id = request.POST['vehicle_id']
    user_id = request.POST['user']
    isUser = User.objects.filter(id=user_id).exists()
    if isUser:
        userObj = User.objects.get(id=user_id)
        user_name=userObj.name
        is_uservehicle = UserVehicle.objects.filter(user=userObj, id=vehicle_id).exists()
        if is_uservehicle:
            vehicle = UserVehicle.objects.get(user=userObj, id=vehicle_id)
            if UserVehicle.objects.filter(user=userObj, id=vehicle_id, refferal_user_num=None).exists():
                vehicle = UserVehicle.objects.get(user=userObj, id=vehicle_id, refferal_user_num=None)
                vehicle.delete()
                activity = userObj.name + " deleted vehicle with registration number " \
                           + vehicle.vehicle_registration_no
                activityObj = User_Activity(user=userObj,activity=activity,category="Vehicle")
                activityObj.save()
                return Response({"error": "0", "message": "vehicle deleted", "data": []})
            else:
                vehicle = UserVehicle.objects.get(user=userObj, id=vehicle_id)
                owner = User.objects.get(id=vehicle.refferal_user_num)
                owner_name=owner.name
                if vehicle.refferal_user_num != None:
                    vehicle.user = owner
                    vehicle.refferal_user_num = None
                    vehicle.save()

                    dict={}
                    vehicle_user_mobile_no=vehicle.user.mobile_number
                    dict["msg"] = "http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=" + str(
                        vehicle_user_mobile_no) + "&message=" + "Hey " + user_name + "! " + owner_name + " has taken back vehicle "+vehicle.vehicle_registration_no
                    arr=[]
                    arr.append(dict)
                    activity = owner.name + " took back vehicle of registration number " \
                               + vehicle.vehicle_registration_no+" from user "+vehicle.user.name
                    activityObj = User_Activity(user=owner, activity=activity,category="Vehicle")
                    activityObj.save()
                    return Response({"error": "3", "message": "vehicle permissions changed", "data": arr})
        else:
            return Response({"error": "2", "message": "Vehicle not exists", "data": []})
    else:
        return Response({"error": "1", "message": "User not exists", "data": []})


@api_view(['POST'])
def refferal_vehicle_details_add(request):
    user_mobile_no = request.POST['user_mobile_no']
    vehicle_no = request.POST['vehicle_registration_no']
    vehicle_owner = request.POST['vehicle_owner_reference_id']
    isuser = User.objects.filter(mobile_number=user_mobile_no).exists()
    isOwner = User.objects.filter(id=vehicle_owner).exists()

    dict = {}
    if isuser:
        if isOwner:
            owner_obj = User.objects.get(id=vehicle_owner)
            isVehicle = UserVehicle.objects.filter(user=owner_obj, vehicle_registration_no=vehicle_no).exists()
            print(isVehicle)
            if isVehicle:
                print("#############1111##############")
                user_obj = User.objects.get(mobile_number=user_mobile_no)
                vehicle = UserVehicle.objects.get(user=owner_obj, vehicle_registration_no=vehicle_no)
                vehicle.refferal_user_num = owner_obj.id
                vehicle.user = user_obj
                vehicle.save()

                activity = owner_obj.name + " gave vehicle of registration number " \
                           + vehicle.vehicle_registration_no + " to user " + user_obj.name
                activityObj = User_Activity(user=owner_obj, activity=activity,category="Vehicle")
                activityObj.save()
                # print("#############222222222##############")
                serializer = VehicleSerializer(instance=vehicle)
                return Response({"error": "0", "message": "Vehicle reference added", "data": serializer.data})
            else:
                return Response({"error": "3",
                                 "message": "Vehicle with this vehicle registration number not exists with vehicle owner " + vehicle_owner,
                                 "data": []})
        else:
            return Response({"error": "2", "message": "Vehicle Owner not exists", "data": []})
    else:
        return Response({"error": "1", "message": "User not exists", "data": []})

@api_view(['POST'])
def refferal_vehicle_msg(request):
    mob1 = request.POST["user_mobile_number"]
    otp = request.POST["otp"]
    owner_id=request.POST["owner_id"]
    vehicle_regd_num=request.POST["vehicle_registered_num"]
    if User.objects.filter(mobile_number=mob1).exists():
        userObj=User.objects.get(mobile_number=mob1)
        if UserVehicle.objects.filter(vehicle_registration_no=vehicle_regd_num).exists():
            vehicle=UserVehicle.objects.get(vehicle_registration_no=vehicle_regd_num)
            if User.objects.filter(id=owner_id).exists():
                owner = User.objects.get(id=owner_id)
                dict = {}

                vehicle_user_mobile_no = vehicle.user.mobile_number
                dict["msg"] = "http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=" + str(
                    mob1) + "&message=" + "Hey " + userObj.name + "! " + owner.name + " gave you this vehicle " + vehicle.vehicle_registration_no + " please confirm with " + str(
                    otp) + " OTP"
                return Response({"error": "0", "message": "Vehicle and user details found", "data": dict})
            else:
                return Response({"error": "3", "message": "Owner not exists", "data": []})
        else:
            return Response({"error": "2", "message": "User Vehicle not exists", "data": []})
    else:
        return Response({"error": "1", "message": "User not exists", "data": []})

@api_view(['POST'])
def vehicle_owner_vehicle_display(request):
    vehicle_owner = request.POST['vehicle_owner_id']
    isOwner = User.objects.filter(id=vehicle_owner).exists()
    print(isOwner,"-----------------")
    if isOwner:
        owner_obj = User.objects.get(id=vehicle_owner)
        print("#################")
        vehicles = UserVehicle.objects.filter(refferal_user_num=owner_obj.id).values()
        if vehicles:
            return Response({"error": "0", "message": "Vehicles details of vehicle owner ", "data": vehicles})
    else:
        return Response({"error": "1", "message": "Vehicle Owner not exists", "data": []})


@api_view(['POST'])
def refferal_user_vehicle_display(request):
    refferal_user = request.POST['refferal_user_id']
    isUser = User.objects.filter(id=refferal_user).exists()
    print(isUser, "-----------------")
    if isUser:
        ref_user_obj = User.objects.get(id=refferal_user)
        print(ref_user_obj, "-----------------")
        vehicles = UserVehicle.objects.filter(user=ref_user_obj.id).values()
        return Response({"error": "0", "message": "Vehicles details of vehicle owner ", "data": vehicles})
    else:
        return Response({"error": "1", "message": "Vehicle Owner not exists", "data": []})


# #############################################___________admin_panel_____######################################

def pz_user_view(request):
    user_wallet = User_Wallet.objects.all()
    # dict= {}
    # arr=[]
    # for x in user:
    #     user_wallet=User_Wallet.objects.filter(user=x.id)
    #     dict[x]=user_wallet
    #     arr.append(dict)
    context={'user':user_wallet}
    return render(request, "User/parkzone_users.html", context)


def pz_user_create(request):
    print("request", request.method)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = User_Form(request.POST, request.FILES)
        # check whether it's valid:

        validations = User_Panel_Validations.validations(form, User, "create")
        if validations == True:
            if form.is_valid():
                form.save()
                return redirect('/User_view', {'dictionary': form})
        else:
            messages.error(request, validations)
            return render(request, 'User/parkzone_user_create.html', {'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form = User_Form()
    return render(request, 'User/parkzone_user_create.html', {'form': form})


def pz_user_edit(request):
    if request.method == "POST":
        id = request.POST['userid']
        user = User.objects.get(id=id)
        form = User_Form(instance=user)
        return render(request, 'User/parkzone_user_update.html', {'User': user, 'form': form})

    else:
        id = request.POST['userid']
        user = User.objects.get(id=id)
        form = User_Form(instance=user)
        return render(request, 'User/parkzone_user_update.html', {'User': user, 'form': form})


def pz_user_update(request):
    if request.method == "POST":
        id = request.POST['userid']
        user = User.objects.get(id=id)
        form = User_Form(request.POST, request.FILES, instance=user)
        validations = User_Panel_Validations.validations(form, User, "update")
        if validations == True:
            if form.is_valid():
                form.save()
                user = User.objects.all()
                return redirect('/User_view')
        else:
            messages.error(request, validations)
            return render(request, 'User/parkzone_user_update.html', {'User': user, 'form': form})


# def pz_user_delete(request):
#     pk = request.POST['userid']
#     user = User.objects.get(id=pk)
#     user.delete()
#     user = User.objects.all()
#     return redirect('/User_view', {'dictionary': user})


def userwallet_create_form(request):
    if request.method == "POST":
        form = User_Wallet_Form(request.POST)
        if form.is_valid():
            form.save()
            userbalance = User_Wallet.objects.last()
            userbalance.balance = int(userbalance.balance + userbalance.transaction_amount)
            userbalance.save()
            messages.success(request, 'Your UserWallet Is Created')
            return redirect('/userwallet_view_form', {'User': form})
        else:

            messages.error(request, form.errors)
            return render(request, 'UserWallet/parkzone_userwallet_create.html', {'form': form})
    else:
        form = User_Wallet_Form(request.POST)
        return render(request, 'UserWallet/parkzone_userwallet_create.html', {'form': form})


def userwallet_view_form(request):
    user = User_Wallet.objects.all()
    query = request.GET.get('user')
    if query:
        user = User_Wallet.objects.filter(
            Q(credit_card_num=query)).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(user, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, "UserWallet/parkzone_userwallet_view.html", {'user': users})


def userwallet_form_edit(request):
    if request.method == "POST":
        id = request.POST['userid']
        user = User_Wallet.objects.get(id=id)
        form = User_Wallet_Form(instance=user)
        return render(request, 'UserWallet/parkzone_userwallet_edit.html', {'user': user, 'form': form})

    else:
        id = request.POST['userid']
        user = User_Wallet.objects.get(id=id)
        form = User_Wallet_Form(instance=user)
        return render(request, 'UserWallet/parkzone_userwallet_edit.html', {'user': user, 'form': form})


def userwallet_update_form(request):
    if request.method == "POST":
        id = request.POST['User']
        userid = request.POST['User_id']
        user = User_Wallet.objects.get(id=id)
        form = User_Wallet_Form(request.POST, instance=user)
        if form.is_valid():
            if form['transaction_type'].value() == "Credit":
                user.balance = int(user.transaction_amount + user.balance)
                form.save()
                userhistory = User_Wallet(myid=userid, balance=form['balance'].value(),
                                          transaction_type=form['transaction_type'].value(),
                                          transaction_amount=form['transaction_amount'].value())
                userhistory.save()
                messages.success(request, 'Your userwallet Is Updated')
                return redirect("userwallet_view_form")
            else:
                user.balance = int(user.balance - user.transaction_amount)
                userhistory = User_Wallet(myid=userid, balance=form['balance'].value(),
                                          transaction_type=form['transaction_type'].value(),
                                          transaction_amount=form['transaction_amount'].value())
                userhistory.save()
                form.save()
            messages.success(request, 'Your userwallet Is Updated')
            return redirect("userwallet_view_form")
        else:
            messages.success(request, 'Your userwallet Update Failed')
            return redirect("userwallet_view_form")


def userwallet_delete_form(request):
    pk = request.POST['userid']
    user = User_Wallet.objects.get(id=pk)
    user.delete()
    messages.success(request, 'Your userwallet Is Deleted')
    user = User_Wallet.objects.all()
    return render(request, 'UserWallet/parkzone_userwallet_view.html', {'user': user})


def user_activity(request):
    if request.method == "POST":
        print("==",request.POST)
        if str(request.POST).__contains__("catlist"):
            userid=request.POST['userid']
            category = request.POST['catlist']
            datefilter=request.POST['datefilter']

            print("category",category)
            if User.objects.filter(id=userid).exists():
                userobj = User.objects.get(id=userid)
                print(userobj)
                ###only datefilter
                arr1 = []
                arr2 = []

                if User_Activity.objects.filter(user=userobj).exists():
                    print("in elif")
                    acts = User_Activity.objects.filter(user=userobj).order_by('-created_at')
                    if len(datefilter)!=0 and not str(category).__contains__('Select Category'):
                        print("both")
                        for x in acts:
                            print("-----",str(x.created_at.date()))
                            print("=====",(datefilter))
                            if x.category.__contains__(category) and str(x.created_at.date())==(datefilter):
                                arr1.append(x)

                        return render(request, 'User/parkzone_user_activity.html',
                                      {'activity': arr1, 'username': userobj.name, 'userid': userobj.id})


                    elif len(datefilter) != 0 and str(category).__contains__('Select Category'):
                        print("date")
                        for x in acts:
                            if str(x.created_at.date()) == (datefilter):
                                arr2.append(x)

                        return render(request, 'User/parkzone_user_activity.html',
                                          {'activity': arr2, 'username': userobj.name, 'userid': userobj.id})



                    elif User_Activity.objects.filter(user=userobj,category=category).exists():
                        print("in if")
                        acts = User_Activity.objects.filter(user=userobj,category=category).order_by('-created_at')
                        return render(request, 'User/parkzone_user_activity.html',
                                  {'activity': acts, 'username': userobj.name, 'userid': userobj.id})
                    else:
                        print("no filter")
                        return render(request, 'User/parkzone_user_activity.html',{'username': userobj.name,'userid': userobj.id})

            else:
                print("nothing")
                return render(request, 'User/parkzone_user_activity.html')
        else:
            pk = request.POST['userid']
            User_Wallet.objects.filter()
            if User.objects.filter(id=pk).exists():
                userobj=User.objects.get(id=pk)

                if User_Activity.objects.filter(user=userobj).exists():
                    acts=User_Activity.objects.filter(user=userobj).order_by('-created_at')
                    return render(request, 'User/parkzone_user_activity.html',{'activity':acts,'username':userobj.name,'userid':userobj.id})
                else:
                    return render(request, 'User/parkzone_user_activity.html',{'username': userobj.name,'userid': userobj.id})
            else:
                return render(request, 'User/parkzone_user_activity.html')
    else:
        return render(request, 'User/parkzone_user_activity.html')

def userWallet_bonus_add(request):
    if request.method == "POST":
        bonus = request.POST['bonus']
        User_Wallet_bonus.objects.all().delete()
        user_wallet_bonus=User_Wallet_bonus()
        user_wallet_bonus.bonus=bonus
        user_wallet_bonus.save()
        return render(request, 'UserWallet/parkzone_add_bonus_wallet_money.html')
    else:
        return render(request, 'UserWallet/parkzone_add_bonus_wallet_money.html')



@Parkzone_middleware
def pz_uservehicle_view(request):
    user = UserVehicle.objects.all()
    query = request.GET.get('user')
    if query:
        user = UserVehicle.objects.filter(
            Q(vehicle_registration_no=query) | Q(driving_lic_number=query) | Q(type=query)).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(user, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, "UserVehicle/parkzone_uservehicle.html", {'user': users})


def pz_uservehicle_create(request):
    if request.method == 'POST':
        form = UserVehicle_Form(request.POST, request.FILES)
        # validations = User_Panel_Validations.vehicle_Validation(form, UserVehicle)
        # if validations == True:
        print(form.errors)
        if form.is_valid():
            print("is valid")
            try:
                form.save()
            except:
                print("  ")
            messages.success(request, 'Vehicle details added successfully')
            return redirect("/UserVehicle_view")
        else:
            messages.error(request, form.errors)
            return render(request, 'UserVehicle/parkzone_uservehicle_create.html', {'form': form})
    else:
        form = UserVehicle_Form(request.POST)
        return render(request, 'UserVehicle/parkzone_uservehicle_create.html', {'form': form})


def pz_uservehicle_edit(request):
    if request.method == "POST":
        id = request.POST['id']
        user = UserVehicle.objects.get(id=id)
        form = UserVehicle_Form(instance=user)
        return render(request, 'UserVehicle/parkzone_uservehicle_update.html', {'User': user, 'form': form})
    else:
        return redirect('pz_uservehicle_view')


def pz_uservehicle_update(request):
    if request.method == "POST":
        id = request.POST['id']
        user = UserVehicle.objects.get(id=id)
        form = UserVehicle_Form(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle Details Updated Successfully')
            return redirect('pz_uservehicle_view')
        else:
            user = UserVehicle.objects.all()
            messages.success(request, 'Vehicle Details Not Updated Successfully')
            return render(request, 'UserVehicle/parkzone_uservehicle_update.html', {'dictionary': user})
    else:
        return redirect('pz_uservehicle_view')


def pz_uservehicle_delete(request):
    if request.method == "POST":
        pk = request.POST['id']
        user = UserVehicle.objects.get(id=pk)
        user.delete()
        messages.success(request, 'Your Profile Is Deleted')
        return redirect('pz_uservehicle_view')
    else:
        return redirect('pz_uservehicle_view')

def user_view1(request):
    id = request.POST['id']
    user = User.objects.filter(id=id)
    array = []
    for x in user:
        data = '<div class="row"> <div class="col-md-4"><h4><label>User Name:</label></h4></div><div class="col-md-8">' + str(x.name) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Country:</label></h4></div><div class="col-md-8">' + str(
            x.country) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>City:</label></h4></div><div class="col-md-8">' + str(
            x.city) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>State:</label></h4></div><div class="col-md-8">' + str(
            x.state) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Mobile Number:</label></h4></div><div class="col-md-8">' + str(
            x.mobile_number) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Age:</label></h4></div><div class="col-md-8">' + str(
            x.age) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Email:</label></h4></div><div class="col-md-8">' + str(
            x.email) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Password:</label></h4></div><div class="col-md-8">' + str(
            x.password) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Confirm Password:</label></h4></div><div class="col-md-8">' + str(
            x.confirm_password) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Facebook Token:</label></h4></div><div class="col-md-8">' + str(
            x.facebook_token) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Google Token:</label></h4></div><div class="col-md-8">' + str(
            x.google_token) + '</div></div>'
        array.append(data)
    return HttpResponse(array)

def vehicle_view1(request):
    id = request.POST['id']
    uservehicle = UserVehicle.objects.filter(id=id)
    array = []
    for x in uservehicle:
        data = '<div class="row"> <div class="col-md-4"><h4><label>User Name:</label></h4></div><div class="col-md-8">' + str(x.user) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Vehical type:</label></h4></div><div class="col-md-8">' + str(
            x.type) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Vehicle Registration No:</label></h4></div><div class="col-md-8">' + str(
            x.vehicle_registration_no) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Type Of Model:</label></h4></div><div class="col-md-8">' + str(
            x.type_of_model) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Vehical Color:</label></h4></div><div class="col-md-8">' + str(
            x.color) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>RC Book No:</label></h4></div><div class="col-md-8">' + str(
            x.rc_book_no) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>RC Book Front File:</label></h4></div><div class="col-md-8">' + str(
            x.rc_book_front_file) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>RC Book Back File:</label></h4></div><div class="col-md-8">' + str(
            x.rc_book_back_file) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Driving Lic Number:</label></h4></div><div class="col-md-8">' + str(
            x.driving_lic_number) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Driving Lic Photo:</label></h4></div><div class="col-md-8">' + str(
            x.driving_lic_photo) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Refferal User Num:</label></h4></div><div class="col-md-8">' + str(
            x.refferal_user_num) + '</div></div>'
        array.append(data)
    return HttpResponse(array)
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render, redirect
import json
# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Watchman.middlewares import Parkzone_middleware
from . import Park_Slot_Owner_Validations, Zone_Panel_Validations
from ParkZoneApp.models import *
from .forms import Park_Slot_Form, Park_Slot_Owner_Form, Zone_Booking_Form
from .serializer import *
from .models import *
from User.models import User, User_Activity
from ParkZoneApp.models import Login
from Society.models import Society
from Zone.models import Park_slot
from User.models import UserVehicle, User_Wallet
import datetime

from django.forms.models import model_to_dict
import random
import pandas as pd
from django.http import HttpResponse


@api_view(['POST'])
def zone_detail_view(request):
    if request.method == "POST":
        id = request.POST['id']
        zone = Park_slot.objects.filter(id=id).values()
        if zone:
            return Response({"error": "0", "message ": "zone details are visible", "data": zone, })
        else:
            return Response({"error": "1", "message": "zone details are not visible"})


@api_view(['POST'])
def servicePackage_detail(request):
    if request.method == "POST":
        socid = request.POST['society_id']
        selected_soc = Society.objects.get(id=socid)
        vehicleid = request.POST['user_vehicle_id']
        vehicle = UserVehicle.objects.get(id=vehicleid)

        arr = []
        dict1 = {}
        dict2 = {}
        dict3 = {}
        dict4 = {}
        if vehicle.type == "1":
            dict1["id"] = 1
            dict1["package_type"] = "Hourly"
            dict1["price"] = selected_soc.two_wheel_hourly_price
            dict2["id"] = 2
            dict2["package_type"] = "Daily"
            dict2["price"] = selected_soc.two_wheel_daily_price
            dict3["id"] = 3
            dict3["package_type"] = "Weekly"
            dict3["price"] = selected_soc.two_wheel_weekly_price
            dict4["id"] = 4
            dict4["package_type"] = "Monthly"
            dict4["price"] = selected_soc.two_wheel_monthly_price
            arr.append(dict1)
            arr.append(dict2)
            arr.append(dict3)
            arr.append(dict4)
        elif vehicle.type == "2":
            dict1["id"] = 1
            dict1["package_type"] = "Hourly"
            dict1["price"] = selected_soc.four_wheel_hourly_price
            dict2["id"] = 2
            dict2["package_type"] = "Daily"
            dict2["price"] = selected_soc.four_wheel_daily_price
            dict3["id"] = 3
            dict3["package_type"] = "Weekly"
            dict3["price"] = selected_soc.four_wheel_weekly_price
            dict4["id"] = 4
            dict4["package_type"] = "Monthly"
            dict4["price"] = selected_soc.four_wheel_monthly_price
            arr.append(dict1)
            arr.append(dict2)
            arr.append(dict3)
            arr.append(dict4)
        return Response({"error": "0", "message ": "Package details found", "data": arr, })


@api_view(['POST'])
def giveFreeTime_Booking(request):
    if request.method == "POST":
        date = request.POST["date"]
        package_id = request.POST["package_id"]
        socid = request.POST['society_id']
        if package_id == 1:
            user_arrive_time = request.POST['time']
        objs = Zone_Booking.objects.filter(booking_date=date)

        selected_soc = Society.objects.get(id=socid)

@api_view(['POST'])
def ZonesView(request):
    tasks = Park_slot.objects.all()
    serializer = ParkSlot_Serializer(tasks, many=True)
    if serializer:
        return Response({"error": "0", "message ": "Your all data", "data": serializer.data, })
    else:
        return Response({"error": "1", "message": "can't find all data"})


@api_view(['POST', 'GET'])
def ZoneRegister(request):
    if request.method == "POST":
        serializer = ParkSlot_Serializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response({"error": "0", "message ": "Your all data", "data": serializer.data, })
        else:
            return Response({"error": "1", "message": "can't find all data"})


@api_view(['POST'])
def ZoneUpdate(request):
    if request.method == "POST":
        id = request.POST['id']
        if not id:
            return Response({"error": "2", "message": "Your ID is NULL"})
        else:
            tasks = Park_slot.objects.get(id=id)
            serializer = ParkSlot_Serializer(instance=tasks, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"error": "0", "message ": "Data Updated", "data": serializer.data, })
            else:
                return Response({"error": "1", "message": "Your Data Is Not Updated"})


@api_view(['DELETE'])
def ZoneDelete(request):
    if request.method == "DELETE":
        id = request.POST['user_id']
        if not id:
            return Response({"error": "2", "message": "Your ID is NULL"})
        else:
            if Park_slot.objects.filter(id=id).exists():
                tasks = Park_slot.objects.get(id=id)
                if tasks:
                    tasks.delete()
                    return Response({"error": "0", "message ": "Data Deleted"})
                else:
                    return Response({"error": "1", "message": "data not deleted"})
            else:
                return Response({"error": "2", "message": "data not Available"})


@api_view(['POST'])
def BookingHistory(request):
    if request.method == "POST":
        userid = request.POST["userid"]
        arr = []
        booking_details = []
        vehicles = ""
        if User.objects.filter(id=userid).exists():
            if UserVehicle.objects.filter(user=userid):
                vehicles = UserVehicle.objects.filter(user=userid)

            if vehicles:
                for x in vehicles:
                    if Zone_Booking.objects.filter(vehicle=x.id).exists():

                        for x in Zone_Booking.objects.filter(vehicle=x.id):
                            dict = {}

                            societyName = x.park_slot.society.name
                            societyAddress = x.park_slot.society.location
                            dict['societyName'] = societyName
                            dict['societyAddress'] = societyAddress
                            dict['booking_id'] = x.id
                            dict['park_slot_id'] = x.park_slot.id
                            dict['vehicle_id'] = x.vehicle.id
                            dict['booking_date'] = x.booking_date
                            dict['activated_package_expire'] = x.activated_package_expire
                            dict['booking_arrival_time'] = x.booking_arrival_time
                            dict['booking_departure_time'] = x.booking_departure_time
                            dict['activated_package'] = x.activated_package
                            dict['booking_amount'] = x.booking_amount
                            dict['otp'] = x.otp
                            dict['booking_status'] = x.booking_status
                            arr.append(dict)
                            subArr = []
                            if Zone_Booking_history.objects.filter(booking_id=x.id).exists():
                                history_list = Zone_Booking_history.objects.filter(booking_id=x.id)
                                for y in history_list:
                                    dict1 = {}
                                    dict1['Checkin_time'] = y.checkin_time
                                    dict1['Checkout_time'] = y.checkout_time
                                    dict1['Checkin_date'] = y.checkin_date
                                    dict1['Checkout_date'] = y.checkout_date
                                    subArr.append(dict1)
                                dict["data"] = (subArr)

                return Response({"error": "0", "message ": "Booking History", "data": arr, })
            else:
                return Response({"error": "2", "message ": "No any bookings for this vehicle", "data": [], })
        else:
            return Response({"error": "1", "message ": "User not exists", "data": [], })


@api_view(['POST', 'GET'])
def BookingRegister(request):
    if request.method == "POST":
        vehicle = request.POST["vehicle"]
        society = request.POST["society"]
        activated_package = request.POST["activated_package"]
        no_of_bookings = request.POST["no_of_bookings"]
        booking_date = request.POST["booking_date"]

        if UserVehicle.objects.filter(id=vehicle).exists():

            vehicle1 = UserVehicle.objects.get(id=vehicle)
            vehicle_type = vehicle1.type
            user = vehicle1.user
            if Society.objects.filter(pk=int(society)).exists():
                society_obj = Society.objects.get(id=society)
                if Society_Secretry.objects.filter(society=society_obj).exists():
                    if Watchman.objects.filter(society=society_obj).exists():
                        park_slot_empty = Park_slot.objects.filter(society=society_obj, availability_status=1,
                                                                   is_reserved_slot=False)
                        if not len(park_slot_empty) == 0:
                            if activated_package == 'Hourly':
                                user_arrival_time = request.POST["booking_arrival_time"]
                                arrival_time = datetime.datetime.strptime(user_arrival_time, '%H:%M:%S').time()
                                soc_opening_time = datetime.datetime.strptime(str(society_obj.opening_time),
                                                                              '%H:%M:%S').time()
                                if arrival_time >= soc_opening_time:

                                    arr = str(arrival_time).split(":")
                                    departure_time = int(arr[0]) + int(no_of_bookings)
                                    departure_time = str(departure_time) + ":" + arr[1] + ":" + arr[2]
                                    depar_time = datetime.datetime.strptime(departure_time, '%H:%M:%S').time()
                                    soc_closing_time = datetime.datetime.strptime(str(society_obj.closing_time),
                                                                                  '%H:%M:%S').time()

                                    if depar_time <= soc_closing_time:
                                        if vehicle_type == '1':
                                            booking_price = society_obj.two_wheel_hourly_price * int(no_of_bookings)
                                        else:
                                            booking_price = society_obj.four_wheel_hourly_price * int(no_of_bookings)
                                        park_slot_empty[0].availability_status = "3"
                                        park_slot_empty[0].save()
                                        booking = Zone_Booking(park_slot=park_slot_empty[0], vehicle=vehicle1,
                                                               booking_arrival_time=arrival_time,
                                                               booking_departure_time=departure_time,
                                                               activated_package="Hourly",
                                                               booking_amount=booking_price, booking_status="Requested",
                                                               booking_date=booking_date, no_of_booking=no_of_bookings,
                                                               activated_package_expire=booking_date )
                                        booking.save()
                                       
                                        activity = user.name+" booked in"+society_obj.name+" with "+booking.activated_package+" package for "\
                                                   +str(booking.booking_arrival_time) +" to "+str(booking.booking_departure_time) +" at "+str(booking.booking_date)
                                        activityObj = User_Activity(user=user, activity=activity,category="Booking")
                                        activityObj.save()
                                    else:
                                        return Response({"error": "8",
                                                         "message": "You can not book because society closing time  " + str(
                                                             soc_closing_time), "data": []})
                                else:
                                    return Response({"error": "7",
                                                     "message": "Society not open yet.Opening time is " + str(
                                                         society_obj.opening_time), "data": []})
                            elif activated_package == 'Monthly':
                                date_1 = datetime.datetime.strptime(booking_date, "%Y-%m-%d")
                                end_date = date_1 + datetime.timedelta(days=(30 * int(no_of_bookings)))
                                expiry_month = str(end_date).split(" ")[0]

                                if vehicle_type == '1':
                                    booking_price = society_obj.two_wheel_monthly_price * int(no_of_bookings)
                                else:
                                    booking_price = society_obj.four_wheel_monthly_price * int(no_of_bookings)
                                park_slot_empty[0].availability_status = "3"
                                park_slot_empty[0].save()
                                booking = Zone_Booking.objects.create(park_slot=park_slot_empty[0], vehicle=vehicle1,
                                                                      booking_date=booking_date,
                                                                      activated_package_expire=expiry_month,
                                                                      activated_package="Monthly",
                                                                      no_of_booking=no_of_bookings,
                                                                      booking_amount=booking_price,
                                                                      booking_status="Requested")
                                booking.save()
                                activity = user.name + " booked in " + society_obj.name + " with " + booking.activated_package + " package for " \
                                           + str(booking.booking_date) + " to " + str(booking.activated_package_expire)
                                activityObj = User_Activity(user=user, activity=activity,category="Booking")
                                activityObj.save()
                            elif activated_package == 'Weekly':
                                date_1 = datetime.datetime.strptime(booking_date, "%Y-%m-%d")
                                end_date = date_1 + datetime.timedelta(days=(6 * int(no_of_bookings)))
                                expiry_month = str(end_date).split(" ")[0]
                                if vehicle_type == '1':
                                    booking_price = society_obj.two_wheel_weekly_price * int(no_of_bookings)
                                else:
                                    booking_price = society_obj.four_wheel_weekly_price * int(no_of_bookings)

                                booking = Zone_Booking(park_slot=park_slot_empty[0], vehicle=vehicle1,
                                                       booking_date=booking_date,
                                                       activated_package_expire=expiry_month,
                                                       activated_package="Weekly",
                                                       booking_amount=booking_price, no_of_booking=no_of_bookings,
                                                       booking_status="Requested")
                                booking.save()
                                activity = user.name + " booked in " + society_obj.name + " with " + booking.activated_package + " package for " \
                                           + str(booking.booking_date) + " to " + str(booking.activated_package_expire)
                                activityObj = User_Activity(user=user, activity=activity,category="Booking")
                                activityObj.save()
                            elif activated_package == 'Daily':
                                date_1 = datetime.datetime.strptime(booking_date, "%Y-%m-%d")
                                end_date = date_1 + datetime.timedelta(days=(int(no_of_bookings)))

                                if vehicle_type == '1':
                                    booking_price = society_obj.two_wheel_daily_price * int(no_of_bookings)
                                else:
                                    booking_price = society_obj.four_wheel_daily_price * int(no_of_bookings)
                                booking = Zone_Booking(park_slot=park_slot_empty[0], vehicle=vehicle1,
                                                       booking_date=booking_date,
                                                       activated_package_expire=end_date.date(),
                                                       activated_package="Daily",
                                                       booking_amount=booking_price, no_of_booking=no_of_bookings,
                                                       booking_status="Requested")
                                booking.save()
                                activity = user.name + " booked in " + society_obj.name + " with " + booking.activated_package + " package for " \
                                           + str(booking.booking_date) + " to " + str(booking.activated_package_expire)
                                activityObj = User_Activity(user=user, activity=activity,category="Booking")
                                activityObj.save()
                            else:
                                return Response({"error": "1", "message": "Booking can't generated", "data": [], })

                            bookingOBj = Zone_Booking.objects.get(id=booking.id)
                            park_slot = bookingOBj.park_slot

                            park_slot.availability_status = "3"
                            park_slot.save()
                            dict_obj = model_to_dict(bookingOBj)

                            return Response(
                                {"error": "0", "message": "Booking generated successfully", "data": dict_obj, })
                        else:

                            if activated_package == 'Hourly':
                                arrival_time = request.POST["booking_arrival_time"]
                                arr = str(arrival_time).split(":")
                                departure_time = int(arr[0]) + int(no_of_bookings)
                                departure_time = str(departure_time) + ":" + arr[1] + ":" + arr[2]
                                user_departure_time = datetime.datetime.strptime(departure_time, '%H:%M:%S').time()
                                user_arrival_time = datetime.datetime.strptime(arrival_time, "%H:%M:%S").time()

                                existing_hourly_booking = Zone_Booking.objects.filter(activated_package="Hourly",booking_date=booking_date)
                                Ignore_list=[]
                                require_list=[]
                                for x in existing_hourly_booking:
                                    if x.booking_arrival_time==user_arrival_time and x.booking_departure_time==user_departure_time:
                                        Ignore_list.append(x.park_slot)
                                    if x.booking_arrival_time < user_arrival_time and x.booking_departure_time > user_arrival_time:
                                        Ignore_list.append(x.park_slot)
                                    if x.booking_arrival_time==user_arrival_time:
                                        Ignore_list.append(x.park_slot)
                                for x in existing_hourly_booking:
                                    if x.park_slot in Ignore_list:
                                        pass
                                    else:
                                        require_list.append(x)

                                soc_closing_time = datetime.datetime.strptime(str(society_obj.closing_time),
                                                                              '%H:%M:%S').time()

                                if user_departure_time <= soc_closing_time:
                                    if vehicle_type == '1':
                                        booking_price = society_obj.two_wheel_hourly_price * int(no_of_bookings)
                                    else:
                                        booking_price = society_obj.four_wheel_hourly_price * int(no_of_bookings)
                                    if require_list!=[]:
                                        require_list[0].park_slot.availability_status = "3"
                                        require_list[0].park_slot.save()
                                        booking = Zone_Booking(park_slot=require_list[0].park_slot, vehicle=vehicle1,
                                                               booking_arrival_time=arrival_time,
                                                               booking_departure_time=departure_time,
                                                               activated_package="Hourly",
                                                               booking_amount=booking_price, booking_status="Requested",
                                                               booking_date=booking_date, no_of_booking=no_of_bookings,
                                                               activated_package_expire=booking_date, )
                                        booking.save()
                                        activity = user.name + " booked in " + society_obj.name + " with " + booking.activated_package + " package for " \
                                                   + str(booking.booking_arrival_time) + " to " + str(booking.booking_departure_time) + " at " + str(booking.booking_date)
                                        activityObj = User_Activity(user=user, activity=activity,category="Booking")
                                        activityObj.save()
                                        park_slot = booking.park_slot

                                        park_slot.availability_status = "3"
                                        park_slot.save()
                                        dict_obj = model_to_dict(booking)
                                        return Response(
                                            {"error": "0", "message": "Booking generated successfully", "data": dict_obj, })
                                    else:
                                        return Response({"error": "9",
                                                         "message": "Sorry!! parking is full.please try after some time" + str(
                                                             soc_closing_time), "data": []})
                                else:
                                    return Response({"error": "9",
                                                     "message": "You can not book because society closing time  " + str(
                                                         soc_closing_time), "data": []})
                            else:
                                return Response(
                                    {"error": "9", "message": "Parking is full try after some time", "data": []})
                    else:
                        return Response({"error": "5",
                                         "message": "Watchman not exist in society so you can not book in this society",
                                         "data": []})
                else:
                    return Response(
                        {"error": "4", "message": "Society Secretry not exists so you can not book in this society",
                         "data": []})
            else:
                return Response({"error": "3", "message": "Society not exists", "data": []})
        else:
            return Response({"error": "2", "message": "Vehicle not exists", "data": []})


@api_view(['POST'])
def user_booking_acknowlegde_msg(request):
    booking_id = request.POST["booking_id"]
    dict = {}
    if Zone_Booking.objects.filter(id=booking_id).exists():
        Booking = Zone_Booking.objects.get(id=booking_id)
        otp = random.randint(100000, 999999)
        Booking.otp = otp
        Booking.save()
        park_slot_obj = Booking.park_slot
        mobile_number = Booking.vehicle.user.mobile_number
        if Booking.activated_package == "Hourly":
            chkin_date = str(Booking.booking_date)
            chkout_date = str(Booking.activated_package_expire)
            chkin_timing = str(Booking.booking_arrival_time)
            chkout_timing = str(Booking.booking_departure_time)
            dict[
                "message"] = "http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=" + str(
                mobile_number) + "&message=" + "Your OTP for Parkzone is " + str(
                otp) + " now you can park your vehicle at " + park_slot_obj.society.name + " today " + \
                             chkin_date + " within " + chkin_timing + "-" + chkout_timing + " hours"
        else:
            chkin_date = str(Booking.booking_date)
            chkout_date = str(Booking.activated_package_expire)
            chkin_timing = str(park_slot_obj.society.opening_time)
            chkout_timing = str(park_slot_obj.society.closing_time)
            dict["message"] = "http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=" + str(
                mobile_number) + "&message=" + "Your booking is complete now you can park your vehicle at " + park_slot_obj.society.name + " for " + \
                             chkin_date + " to " + chkout_date + " within " + chkin_timing + "-" + chkout_timing

        return Response({"error": "0", "message": "Booking details found", "data": dict})
    else:
        return Response({"error": "2", "message": "Booking details not found something went wrong", "data": []})


@api_view(['POST'])
def user_otp_verify(request):
    otp = request.POST['otp']
    slot_id = request.POST['slot_id']
    isslot = Park_slot.objects.filter(id=slot_id).exists()
    if isslot:
        park_slot = Park_slot.objects.get(id=slot_id)
        if Zone_Booking.objects.filter(park_slot=park_slot, otp=otp).exists():
            booking_obj = Zone_Booking.objects.get(park_slot=park_slot, otp=otp)
            user = booking_obj.vehicle.user
            dict = {}
            dict['user_id'] = user.id
            dict['vehicle_id'] = booking_obj.vehicle.id
            wallet = User_Wallet.objects.get(user=user.id)
            dict['wallet_id'] = wallet.id
            dict['booking_id'] = booking_obj.id
            return Response({"error": "0", "message": "otp verified", "data": dict, })
        else:
            return Response({"error": "1", "message": "otp not varified something went wrong"})
    else:
        return Response({"error": "2", "message": "Park Slot not exists", "data": []})


@api_view(['POST'])
def user_checkout(request):

    slotid = request.POST['slot_id']
    bookid = request.POST['booking_id']

    isSlot = Park_slot.objects.filter(id=slotid).exists()
    if isSlot:

        slot = Park_slot.objects.get(id=slotid)

        isbooking = Zone_Booking.objects.filter(id=bookid, park_slot=slot).exists()
        if isbooking:
            booking = Zone_Booking.objects.get(id=bookid, park_slot=slot)
            user = booking.vehicle.user
            userid = user.id
            wallet = User_Wallet.objects.get(user=userid)
            wallet_id = wallet.id
            dict = {}
            dict['wallet_id'] = wallet_id
            dict['user_id'] = userid
            checkout_time = request.POST['checkout_time']

            checkout_date = request.POST['checkout_date']
            if booking.activated_package == "Hourly":
                slot_obj = booking.park_slot
                slot_obj.availability_status = "1"
                slot_obj.save()
                booking.booking_status = "Paid"
                booking.save()
                activity = user.name + " checkout from " + slot_obj.society.name +  " at " + checkout_date +" "+ checkout_time
                activityObj = User_Activity(user=user, activity=activity,category="Booking")
                activityObj.save()
                if booking.booking_departure_time == checkout_time and booking.activated_package_expire == checkout_date:
                    dict['booking_amount'] = booking.booking_amount
                    return Response({"error": "0", "message": "Checkout details ", "data": dict, })
                else:
                    df = pd.DataFrame({
                        'date': [booking.activated_package_expire, checkout_date]
                    })

                    # Convert to datetime objects
                    df['date'] = df['date'].apply(lambda x: datetime.datetime.strptime(str(x), "%Y-%m-%d"))

                    # Extract and subtract dates
                    d1 = df.loc[0, 'date']
                    d2 = df.loc[1, 'date']

                    date_diff = (d2 - d1).days

                    time_diff = datetime.datetime.strptime(str(checkout_time), '%H:%M:%S') - datetime.datetime.strptime(
                        str(booking.booking_arrival_time), '%H:%M:%S')

                    extrahour = str(time_diff).split(":")[0]

                    if date_diff == 0:
                        calc = 0
                    else:
                        calc = ((86400 * date_diff) / (3600)) - 24
                    if extrahour == "0":
                        Amount = booking.booking_amount
                    elif extrahour.__contains__("day"):
                        arr = extrahour.split(", ")[1]
                        Amount = booking.booking_amount + (calc + float(arr)) * (booking.booking_amount)
                    else:
                        Amount = booking.booking_amount + float(extrahour) * (booking.booking_amount)
                    dict['booking_amount'] = Amount
                    historyOBJ = Zone_Booking_history(booking_id=booking.id,
                                                      checkin_time=booking.park_slot.society.opening_time,
                                                      checkin_date=booking.booking_date,
                                                      checkout_time=checkout_time, checkout_date=checkout_date)
                    historyOBJ.save()

                    if float(wallet.balance) > Amount:
                        booking.booking_amount = Amount
                        booking.save()
                        return Response({"error": "0", "message": "Checkout details", "data": dict, })
                    else:
                        return Response(
                            {"error": "1", "message": "Your balance is not enough.please credit balance", "data": [], })
            else:

                if str(checkout_date) == str(booking.activated_package_expire) and str(checkout_time) == str(
                        slot.society.closing_time):
                    slot_obj = booking.park_slot
                    slot_obj.availability_status = "1"
                    slot_obj.save()
                    booking.booking_status = "Paid"

                    dict['booking_amount'] = booking.booking_amount
                    booking.save()
                    return Response({"error": "0",
                                     "message": "your " + str(booking.activated_package) + " is expired on " + str(
                                         booking.activated_package_expire), "data": [], })
                else:
                    slot_obj = booking.park_slot
                    slot_obj.availability_status = "3"
                    slot_obj.save()
                    booking.booking_status = "Requested"
                    booking.save()
                    if Zone_Booking_history.objects.filter(checkin_date=checkout_date, booking_id=booking.id,
                                                           checkout_date=None).exists():
                        historyOBJ = Zone_Booking_history.objects.get(checkin_date=checkout_date, booking_id=booking.id,
                                                                      checkout_date=None)
                        if historyOBJ.checkout_date == None and historyOBJ.checkout_time == None:
                            historyOBJ.checkout_time = checkout_time
                            historyOBJ.checkout_date = checkout_date
                            historyOBJ.save()
                        serializer = Booking_history_Serializer(instance=historyOBJ)
                        return Response({"error": "3", "message": "Booking history found",
                                         "data": serializer.data, })
                    elif Zone_Booking_history.objects.filter(checkin_date=checkout_date, booking_id=booking.id,
                                                             checkout_date=checkout_date).exists():
                        historyOBJ = Zone_Booking_history(booking_id=booking.id,
                                                          checkin_time=booking.park_slot.society.opening_time,
                                                          checkin_date=booking.booking_date,
                                                          checkout_time=checkout_time, checkout_date=checkout_date)
                        historyOBJ.save()
                        serializer = Booking_history_Serializer(instance=historyOBJ)
                        return Response({"error": "3", "message": "Booking history found",
                                         "data": serializer.data, })
                    else:
                        return Response({"error": "3", "message": "Booking history not found",
                                         "data": [], })

        else:
            return Response({"error": "2", "message": "Booking not available something went wrong", "data": [], })
    else:
        return Response({"error": "1", "message": "Parking slot not found", "data": [], })


@api_view(['POST'])
def BookingUpdate(request):
    id = request.POST['id']
    if not id:
        return Response({"error": "2", "message": "Your id is blank or null", "data": []})
    else:
        tasks = Zone_Booking.objects.get(id=id)

        serializer = Booking_Serializer(instance=tasks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"error": "0", "message ": "Booking details updated successfully", "data": serializer.data, })
        else:
            return Response({"error": "1", "message": "Booking details not updated", "data": []})


@api_view(['DELETE'])
def Booking_Cancel(request):
    if request.method == "DELETE":
        id = request.POST['id']
        if Zone_Booking.objects.filter(id=id).exists():
            tasks = Zone_Booking.objects.get(id=id)
            if tasks:
                tasks.delete()
                return Response({"error": "0", "message ": "Booking canceled"})
            else:
                return Response({"error": "1", "message": "Booking not canceled", "data": []})


@api_view(['POST'])
def booking_detail_view(request):
    if request.method == "POST":
        id = request.POST['booking_id']
        booking = Zone_Booking.objects.filter(id=id).values()

        parkslot_id = booking[0]['park_slot_id']
        slot = Park_slot.objects.get(id=parkslot_id)
        soc = slot.society
        soc_id = soc.id
        data = list(booking)
        dict = {}
        data[0]['society_id'] = soc_id
        data[0]['Park_slot_name'] = slot.slot_name
        data[0]['slot_lat'] = slot.latitude
        data[0]['slot_long'] = slot.langitude
        if booking:
            return Response({"error": "0", "message ": "Booking details are visible", "data": data, })
        else:
            return Response({"error": "1", "message": "Booking details are not visible", "data": []})


@api_view(['POST'])
def reserved_slots_list(request):
    if request.method == "POST":
        id = request.POST['society_id']
        if Society.objects.filter(id=id).exists():
            soc_obj = Society.objects.get(id=id)
            if Park_slot.objects.filter(society=soc_obj, is_reserved_slot=True).exists():
                slots = Park_slot.objects.filter(society=soc_obj, is_reserved_slot=True).values()
                return Response({"error": "0", "message": "Reserved slot list", "data": slots})
            else:
                return Response({"error": "2", "message": "No any reserved park slots found", "data": []})
        else:
            return Response({"error": "1", "message": "No any society found", "data": []})




#######################################################__________admin_panel_____________########################################

@Parkzone_middleware
def Zone_view(request):
    if request.method == "POST":

        id = request.POST['society']
        zone = Park_slot.objects.filter(society=id)

        society = Society.objects.all()
        return render(request, 'zone/parkzone_zoneview.html',{'zone': zone, 'society': society})
    else:
        society = Society.objects.all()
        return render(request, 'zone/parkzone_zoneview.html', {'society': society})


@Parkzone_middleware
def Zone_create(request):
    if request.method == "POST":

        form = Park_Slot_Form(request.POST)

        if form.is_valid():
            form.save()
            return redirect('Zone_view')
        else:
            messages.success(request, form.errors)

    else:
        form = Park_Slot_Form()
        return render(request, 'zone/parkzone_zonecreate.html', {'form': form})


def Zone_delete(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Park_slot.objects.get(id=id)
        data.delete()

        return redirect("Zone_view")
    else:
        return redirect("Zone_view")


def Zone_edit(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Park_slot.objects.get(id=id)
        form = Park_Slot_Form(instance=data)
        return render(request, 'zone/parkzone_zoneedit.html', {'data': data, 'form': form})
    else:
        return redirect('Zone_view')


def Zone_update(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Park_slot.objects.get(id=id)
        form = Park_Slot_Form(request.POST, request.FILES, instance=data)

        if form.is_valid():
            form.save()
            return redirect("Zone_view")
        else:
            messages.error(request, "Zone details not valid")


@Parkzone_middleware
def Booking_view(request):
    if request.method == "POST":
        id = request.POST['society']
        soc = Society.objects.get(id=id)
        slot = Park_slot.objects.filter(society=soc)

        arr = []
        society = Society.objects.all()
        for x in slot:

            if Zone_Booking.objects.filter(park_slot=x).exists():
                booking = Zone_Booking.objects.filter(park_slot=x)
                for y in booking:
                    arr.append(y)
        return render(request, 'booking/parkingzone_bookingview.html',
                      {'booking': arr, 'society': society, 'soc_name': soc.name,
                       'message': 'No any booking found for society'})
    else:
        society = Society.objects.all()
        return render(request, 'booking/parkingzone_bookingview.html', {'society': society})


def show_booking_history(request):
    if request.method == "POST":
        id = request.POST['history']

        if Zone_Booking_history.objects.filter(booking_id=id).exists():
            history_record = Zone_Booking_history.objects.filter(booking_id=id)
            booking = Zone_Booking.objects.get(id=id)
            return render(request, 'booking/parkingzone_bookinghistory.html', {
                'booking_history': history_record,
                'booking_name': booking.vehicle.user.name,
                'booking_package': booking.activated_package,
            })
        else:

            return redirect('Booking_view')


def parkslot_owner_create_form(request):
    if request.method == "POST":
        form = Park_Slot_Owner_Form(request.POST, request.FILES)
        validations = Park_Slot_Owner_Validations.park_slot_owner_validations(form, Park_Slot_Owner, "create")

        if validations == True:
            if form.is_valid():
                object = form.save()

                objectid = object.id
                query = Login(number=objectid, email=form['email'].value(), password=form['password'].value(),
                              type='parkingslotowner')
                query.save()

                messages.success(request, 'Parking Slot Owner Created')
                return redirect("parkslot_owner_view_form")
            else:
                messages.success(request, form.errors)
        else:
            messages.error(request, validations)
            return render(request, 'ParkSlotOwner/pz_park_slot_owner_create.html', {'form': form})
    else:
        form = Park_Slot_Owner_Form()
    return render(request, 'ParkSlotOwner/pz_park_slot_owner_create.html', {'form': form})


def parkslot_owner_view_form(request):
    email = request.session.get('email')
    if Society_Secretry.objects.filter(email=email).exists():
        ss = Society_Secretry.objects.get(email=email)
        society = ss.society
        slots = Park_slot.objects.filter(society=society)

        park_slot_owner_obj = Park_Slot_Owner()
        for x in slots:
            if Park_Slot_Owner.objects.filter(park_slot=x.id).exists():
                park_slot_owner_obj = Park_Slot_Owner.objects.filter(park_slot=x)




                return render(request, "ParkSlotOwner/pz_park_slot_owner_view.html",
                              {'park_slot_owners': park_slot_owner_obj})
    else:
        owners = Park_Slot_Owner.objects.all()
        return render(request, "ParkSlotOwner/pz_park_slot_owner_view.html", {'park_slot_owners': owners})


def parkslot_owner_delete_form(request):
    pk = request.POST['userid']

    parking_slot_owner = Park_Slot_Owner.objects.get(number=pk)
    login = Login.objects.get(id=pk)
    parking_slot_owner.delete()
    login.delete()
    messages.success(request, 'Parking Slot Owner Profile Is Deleted')
    return redirect("parkslot_owner_view_form")


def parkslot_owner_edit_form(request):
    if request.method == "POST":
        id = request.POST['userid']
        parkslot_owner = Park_Slot_Owner.objects.get(id=id)
        form = Park_Slot_Owner_Form(instance=parkslot_owner)
        return render(request, 'ParkSlotOwner/pz_park_slot_owner_edit.html',
                      {'parksolt_owner': parkslot_owner, 'form': form})

    else:
        id = request.POST['userid']
        parkslot_owner = Park_Slot_Owner.objects.get(id=id)
        form = Park_Slot_Owner_Form(instance=parkslot_owner)
        return render(request, 'ParkSlotOwner/pz_park_slot_owner_edit.html',
                      {'parksolt_owner': parkslot_owner, 'form': form})


def parkslot_owner_update_form(request):
    if request.method == "POST":
        id = request.POST['ParkSlot']

        park_slot_owner = Park_Slot_Owner.objects.get(id=id)
        form = Park_Slot_Owner_Form(request.POST, request.FILES, instance=park_slot_owner)
        validations = Park_Slot_Owner_Validations.park_slot_owner_validations(form, Park_Slot_Owner, "update")
        if validations == True:
            if form.is_valid():
                object = form.save()
                loginupdate = Login.objects.get(number=object.id)

                loginupdate.email = form['email'].value()
                loginupdate.password = form['password'].value()
                loginupdate.save()
                messages.success(request, 'Parking Slot Owner Profile Edited')
                return redirect("parkslot_owner_view_form")
        else:
            messages.error(request, validations)
            return render(request, 'ParkSlotOwner/pz_park_slot_owner_edit.html',
                          {'park_slot_owner': park_slot_owner, 'form': form})


def pz_society_detail_view(request):
    park_slot_owner = request.session.get('email')
    park_slot_owner_records = Park_Slot_Owner.objects.get(email=park_slot_owner)
    parking_slot = Park_slot.objects.get(id=park_slot_owner_records.park_slot_id)
    societyview = Society.objects.filter(id=parking_slot.society_id)
    context = {
        'societyview': societyview
    }
    return render(request, 'zone/pz_society_view.html', context)


def parkzone_user_view(request):
    email = request.session.get('email')
    parkingslotownerrecord = Park_Slot_Owner.objects.get(email=email)
    bookingrecord = Zone_Booking.objects.filter(park_slot_id=parkingslotownerrecord.park_slot_id)
    if bookingrecord:
        data = []
        for zrecord in bookingrecord:
            user_id = zrecord.vehicle.user.id
            data.append(user_id)
        for newdata in data:
            newdata = User.objects.filter(id=newdata)
            query = request.GET.get('newdata')
            if query:
                newdata = User.objects.filter(
                    Q(name=query) | Q(city=query) |
                    Q(mobile_number=query) | Q(email=query)).order_by('-id')
            page = request.GET.get('page', 1)
            paginator = Paginator(newdata, 10)
            try:
                newdata = paginator.page(page)
            except PageNotAnInteger:
                newdata = paginator.page(1)
            except EmptyPage:
                newdata = paginator.page(paginator.num_pages)
        return render(request, 'zone/parkzone_user_record.html', {'newdata': newdata, 'data': newdata})
    return render(request, 'zone/parkzone_user_record.html')


@Parkzone_middleware
def parkzone_park_slot_detail_view(request):
    email = request.session.get('email')
    data = Park_Slot_Owner.objects.get(email=email)
    park_slot = Park_slot.objects.filter(id=data.park_slot_id)
    query = request.GET.get('park_slot')
    if query:
        park_slot = Park_slot.objects.filter(
            Q(slot_name=query)).order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(park_slot, 10)
    try:
        park_slots = paginator.page(page)
    except PageNotAnInteger:
        park_slots = paginator.page(1)
    except EmptyPage:
        park_slots = paginator.page(paginator.num_pages)
    return render(request, 'zone/pz_park_slot_detail_view.html', {'park_slot': park_slot})


@Parkzone_middleware
def parkzone_park_slot_owner_detail_view(request):
    email = request.session.get('email')
    park_slot_owner = Park_Slot_Owner.objects.get(email=email)
    return render(request, 'zone/pz_park_slot_owner_detail_view.html', {'park_slot_owner': park_slot_owner})


@Parkzone_middleware
def parkzone_park_slot_owner_detail_edit(request):
    id = request.POST['id']
    if request.method == "POST":
        data = Park_Slot_Owner.objects.get(id=id)
        form = Park_Slot_Owner_Form(instance=data)
        return render(request, 'zone/pz_park_slot_owner_detail_update.html', {'park_zone_owner': data, 'form': form})
    else:
        return redirect('parkzone_park_slot_owner_detail_view')


def parkzone_park_slot_owner_detail_update(request):
    email = request.session.get('email')
    if request.method == "POST":
        id = request.POST['ParkSlot']
        data = Park_Slot_Owner.objects.get(id=id)
        form = Park_Slot_Owner_Form(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            loginupdate = Login.objects.get(id=id)
            loginupdate.email = form['email'].value()
            loginupdate.password = form['password'].value()
            loginupdate.save()
            if email != loginupdate.email:
                messages.success(request, 'Parking Slot Owner Profile Edited Successfully')
                return redirect("logout")
            else:
                messages.success(request, 'Your Profile Is Edited')
                return redirect('parkzone_park_slot_owner_detail_view')
        else:
            messages.success(request, 'Your Profile Is Invalid')
            return redirect('parkzone_park_slot_owner_detail_view')
    else:
        return redirect('parkzone_park_slot_owner_detail_view')

def owner_view1(request):
    id = request.POST['id']
    park_slot_owner = Park_Slot_Owner.objects.filter(id=id)
    array = []
    for x in park_slot_owner:
        data = '<div class="row"> <div class="col-md-4"><h4><label>Name:</label></h4></div><div class="col-md-8">' + str(x.name) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Park Slot:</label></h4></div><div class="col-md-8">' + str(
            x.park_slot) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Address:</label></h4></div><div class="col-md-8">' + str(
            x.address) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>City:</label></h4></div><div class="col-md-8">' + str(
            x.city) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Mobile Number:</label></h4></div><div class="col-md-8">' + str(
            x.mobile_number) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Email:</label></h4></div><div class="col-md-8">' + str(
            x.email) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Password:</label></h4></div><div class="col-md-8">' + str(
            x.password) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Aadhar Card Currently:</label></h4></div><div class="col-md-8">' + str(
            x.aadhar_card) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Aadhar Number:</label></h4></div><div class="col-md-8">' + str(
            x.aadhar_num) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Bank Name:</label></h4></div><div class="col-md-8">' + str(
            x.bank_name) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Branch:</label></h4></div><div class="col-md-8">' + str(
            x.branch) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Account Number:</label></h4></div><div class="col-md-8">' + str(
            x.account_number) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>IFSC Code:</label></h4></div><div class="col-md-8">' + str(
            x.ifsc_code) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Change:</label></h4></div><div class="col-md-8">' + str(
            x.commision) + '</div></div>'
        array.append(data)
    return HttpResponse(array)

def Zone_popupview(request):
    id = request.POST['id']
    park_slot = Park_slot.objects.filter(id=id)
    array = []
    for x in park_slot:
        data = '<div class="row"> <div class="col-md-4"><h4><label>Society Name:</label></h4></div><div class="col-md-8">' + str(
            x.society) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Availability Status:</label></h4></div><div class="col-md-8">' + str(
            x.availability_status) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Slot Name:</label></h4></div><div class="col-md-8">' + str(
            x.slot_name) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Latitude:</label></h4></div><div class="col-md-8">' + str(
            x.latitude) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Langtitude:</label></h4></div><div class="col-md-8">' + str(
            x.langitude) + '</div></div>'
        array.append(data)
    return HttpResponse(array)
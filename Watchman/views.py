from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict

from Zone.models import Park_slot, Zone_Booking,Zone_Booking_history
from Zone.serializer import Booking_history_Serializer
from . import Watchman_Panel_Validations
from .forms import Watchman_Form
from .middlewares import Parkzone_middleware
from .models import *
from Society.models import *
from User.models import *
from .serializer import Watchman_Serializer
from .watchman_API_Validation import watchmanAPI_Validations
import datetime
path1 = "http://127.0.0.1:8000/media/"
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core import serializers
from Zone.serializer import ParkSlot_Serializer
from django.http import HttpResponse

@api_view(['POST'])
def WatchmanView(request):
    tasks = Watchman.objects.all()
    serializer = Watchman_Serializer(tasks, many=True)
    if serializer:
        return Response({"error": "0", "message ": "Your all data", "data": serializer.data, })
    else:
        return Response({"error": "1", "message": "can't find all data"})


@api_view(['POST'])
def WatchmanRegister(request):
    if request.method == "POST":
        serializer = Watchman_Serializer(data=request.data)
        validationMessage = watchmanAPI_Validations(request, Watchman)
        if validationMessage == True:
            if serializer.is_valid():
                serializer.save()
                data = Watchman.objects.values().last()
                data['aadhar_card'] = path1 + data['aadhar_card']
                data['passport_photo'] = path1 + data['passport_photo']
                return Response(
                    {"error": "0", "message ": "Watchman registered successfully", "data": serializer.data, })
            else:
                return Response({"error": "1", "message": "Watchman is not registered , somthing went wrong"})
        else:
            varray = validationMessage.split(":")
            return Response({"error": varray[0], "message": varray[1]})


@api_view(['POST'])
def WatchmanUpdate(request):
    id = request.data['id']
    if not id:
        return Response({"error": "2", "message": "Your ID is NULL"})
    else:
        if Watchman.objects.filter(id=id).exists():
            tasks = Watchman.objects.get(id=id)
            serializer = Watchman_Serializer(instance=tasks, data=request.data)
            validationMessage = watchmanAPI_Validations(request, Watchman)
            if validationMessage == True:
                if serializer.is_valid():
                    serializer.save()

                    return Response(
                        {"error": "0", "message ": "Watchman details updated successfully", "data": serializer.data, })
                else:
                    return Response({"error": "1", "message": "Watchman details not updated"})
            else:
                varray = validationMessage.split(":")
                return Response({"error": varray[0], "message": varray[1]})


@api_view(['DELETE'])
def WatchmanDelete(request):
    if request.method == "DELETE":
        id = request.POST['id']
        if not id:
            return Response({"error": "2", "message": "Your ID is NULL"})
        else:
            if Watchman.objects.filter(id=id).exists():
                tasks = Watchman.objects.get(id=id)
                if tasks:
                    tasks.delete()
                    return Response({"error": "0", "message ": "Data Deleted"})
                else:
                    return Response({"error": "1", "message": "Data Not deleted"})
            else:
                return Response({"error": "2", "message": "Dat Not Available"})


@api_view(['POST'])
def watchman_detail_view(request):
    pk = request.POST['id']
    watchman = Watchman.objects.filter(id=pk).values()
    if watchman:
        return Response({"error": "0", "message ": "Watchman detail visible", "data": watchman, })
    else:
        return Response({"error": "1", "message": "Watchman detail not visible"})


@api_view(['POST'])
def watchman_Login(request):
    if request.method == "POST":
        mobilenumber = request.POST['mobile_number']
        password = request.POST['password']
        if not (mobilenumber and password):
            return Response({"error": "2", "message": "Your Mobile Number Or Password Is Blank", "data": []})
        else:
            if Watchman.objects.filter(mobile_number=mobilenumber, password=password).exists():
                data = Watchman.objects.filter(mobile_number=mobilenumber, password=password).values()
                return Response({"error": "0", "message": "You Are Now Login Successfully", "data": data})
            else:
                return Response({"error": "1", "message": "Your User_name or Password Is Incorrect", "data": []})


@Parkzone_middleware
def watchman_create(request):
    if request.method == "POST":
        form = Watchman_Form(request.POST, request.FILES)
        if len(form['mobile_number'].value()) < 10:
            messages.success(request, 'Invalid Mobile Number')
            return render(request, 'watchman/parkzone_watchmancreate.html', {'form': form})
        else:
            if len(form['aadhar_number'].value()) < 12:
                messages.success(request, 'Invalid AadharCard Number')
                return render(request, 'watchman/parkzone_watchmancreate.html', {'form': form})
            elif form.is_valid():
                form.save()
                messages.success(request, 'Your Profile Is Created')
                return redirect('watchman_view')
            else:
                messages.success(request, 'Your Register Failed')
                return render(request, 'watchman/parkzone_watchmancreate.html', {'form': form})
    else:
        form = Watchman_Form()
        return render(request, 'watchman/parkzone_watchmancreate.html', {'form': form})


@api_view(['POST'])
def watchman_Society_details(request):
    if request.method == "POST":
        watchman_id = request.POST['watchman_id']
        watchmanObj = Watchman.objects.get(id=watchman_id)
        society = watchmanObj.society
        print("society---", society)
        dict = {}
        dict["society_id"] = society.id

        return Response({"error": "2", "message": "Your Mobile Number Or Password Is Blank", "data": dict})


@api_view(['POST'])
def zone_status(request):
    if request.method == "POST":
        soc_id = request.POST['society_id']
        today_date=request.POST['date']
        today_time=request.POST['time']
        time = datetime.datetime.strptime(today_time, '%H:%M:%S').time()
        date=datetime.datetime.strptime(today_date, "%Y-%m-%d").date()
        zones = Park_slot.objects.filter(society=soc_id)
        zones_list=list(zones)
        answer=[]
        for zone in zones_list:
            dict = {}
            bookingObjs = Zone_Booking.objects.filter(park_slot=zone.id)
            bookinglist=list(bookingObjs)
            dict['zone_id']=zone.id
            dict['society_id']=zone.society.id
            dict['availability_status']=zone.availability_status
            dict['has_owner']=zone.has_owner
            dict['is_reserved_slot']=zone.is_reserved_slot
            dict['slot_name']=zone.slot_name
            dict['lat'] = zone.latitude
            dict['long'] = zone.langitude
            dict['created_at'] =zone.created_at
            dict['updated_at'] =zone.updated_at
            for booking in bookinglist:
                if booking.activated_package=="Hourly":
                    if date >= booking.booking_date and date <= booking.activated_package_expire:
                        if time >= booking.booking_arrival_time and time <= booking.booking_departure_time:
                            dict['booking_id'] =booking.id
                            dict['vehicle_id']=booking.vehicle.id
                            dict['user_id']=booking.vehicle.user.id
                            wallet=User_Wallet.objects.get(user=booking.vehicle.user)
                            dict['wallet_id']=wallet.id
                else:
                    if date >= booking.booking_date and date <= booking.activated_package_expire:
                        dict['booking_id'] = booking.id
                        dict['vehicle_id'] = booking.vehicle.id
                        dict['user_id'] = booking.vehicle.user.id
                        wallet = User_Wallet.objects.get(user=booking.vehicle.user)
                        dict['wallet_id'] = wallet.id
            answer.append(dict)


        if answer!=[]:
            return Response({"error": "0", "message ": "zone details are visible", "data": answer, })
        else:
            return Response({"error": "1", "message": "zone details are not visible", "data": []})


@api_view(['POST'])
def zone_booked(request):
    if request.method == "POST":
        key_taken = request.POST['key']
        slot_id = request.POST['slot_id']
        if key_taken == "True":
            if Park_slot.objects.filter(id=slot_id).exists():
                zone = Park_slot.objects.get(id=slot_id)
                print(zone)
                zone.availability_status = "2"
                zone.save()
                if Zone_Booking.objects.filter(park_slot=zone.id, booking_status="Requested").exists() :
                    print("in if requested")
                    book = Zone_Booking.objects.get(park_slot=zone.id, booking_status="Requested")
                    book.booking_status = "Booked"
                    book.save()
                    user_obj=book.vehicle.user
                    if book.activated_package == "Hourly":

                        dict = {}
                        dict['slot_id'] = slot_id
                        dict['availability_status'] = zone.availability_status
                        dict['user_alert']="http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=" + str(
                user_obj.mobile_number) + "&message=" + "your vehicle "+ book.vehicle.vehicle_registration_no +" is checked in and key is taken thanks for parking"
                        return Response({"error": "0", "message ": "Zone booked", "data": dict, })
                    else:
                        print("in if other")
                        checkin_date = request.POST['checkin_date']
                        checkin_time = request.POST['checkin_time']

                        historyOBJ = Zone_Booking_history(booking_id=book.id,
                                                     checkin_time=checkin_time,
                                                     checkin_date=checkin_date)
                        historyOBJ.save()
                        serializer = Booking_history_Serializer(instance=historyOBJ)
                        return Response({"error": "3", "message": "Booking history updated",
                                             "data": serializer.data, })

                else:
                    return Response(
                        {"error": "1", "message ": "Booking details not found somthing went wrong", "data": [], })
            else:
                return Response({"error": "1", "message ": "Parking slot not exists", "data": [], })
        elif key_taken == "False":
            return Response({"error": "0", "message ": "User took back his keys", "data": [], })


@api_view(['POST'])
def transfer_vehicle(request):
    booking_id=request.POST['booking_id']
    vehicle_id=request.POST['vehicle_id']
    reserve_slot_id=request.POST['reserve_slot_id']
    soc_id=request.POST['soc_id']
    if Society.objects.filter(id=soc_id).exists():
        society=Society.objects.get(id=soc_id)
        if Park_slot.objects.filter(id=reserve_slot_id,society=society.id,is_reserved_slot=True).exists():
            reserve_slot=Park_slot.objects.get(id=reserve_slot_id, society=society.id)
            if Zone_Booking.objects.filter(id=booking_id,vehicle=vehicle_id).exists():
                booking=Zone_Booking.objects.get(id=booking_id, vehicle=vehicle_id)
                if booking.activated_package=="Hourly":
                    vehicle=booking.vehicle
                    if UserVehicle.objects.filter(id=vehicle.id).exists():
                        dict={}
                        reserve_slot.availability_status="2"
                        reserve_slot.save()
                        booked_slot=booking.park_slot
                        booked_slot.availability_status = "1"
                        booked_slot.save()
                        booking.park_slot=reserve_slot
                        booking.save()
                        user=vehicle.user
                        mob_num=user.mobile_number
                        dict["message"] = "http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=" + str(
                            mob_num) + "&message=" + " Hey ! " + user.name + " Your vehicle parked at reserved slot"

                        return Response({'error': '0', 'message': "Vehicle Tranfer ot reserve slot succesfully", 'data': dict})
                    else:
                        return Response({'error': '5', 'message': "Vehicle not exists", 'data': []})
                else:
                    return Response({'error': '4', 'message': "You can not transfer this vehicle", 'data': []})
            else:
                return Response({'error': '3', 'message': "Booking not exists", 'data': []})
        else:
            return Response({'error': '2', 'message': "ParkSlot not exists", 'data': []})

    else:
        return Response({'error':'1','message':"Society not exists",'data':[]})

@api_view(['POST'])
def saveSlotMarks(request):
    if request.method == "POST":
        lat = request.POST['lat']
        lang= request.POST['long']
        slot_id=request.POST['slot_id']
        watchman_id=request.POST['watchman_id']
        if Watchman.objects.filter(id=watchman_id).exists():
            watch_obj = Watchman.objects.get(id=watchman_id)
            if Park_slot.objects.filter(id=slot_id).exists():
                slotObj=Park_slot.objects.get(id=slot_id)
                # socObj=slotObj.society
                slotObj.latitude=lat
                slotObj.langitude=lang
                slotObj.save()
                serializers=ParkSlot_Serializer(instance=slotObj)
                return Response({"error": "0", "message": "Park slot lat long saved", "data": serializers.data})
            else:
                return Response({"error": "2", "message": "Park slot not found", "data": []})
        else:
            return Response({"error": "1", "message": "Watchman not found", "data": []})

############################################################____admin_panel_________###############################################

@Parkzone_middleware
def watchman_create(request):
    if request.method == "POST":
        form = Watchman_Form(request.POST, request.FILES)
        # validations = Watchman_Panel_Validations.watchman_validations(form, 0, "create")
        # if validations == True:
        print(form.errors)
        if form.is_valid():
            print("in if")
            form.save()
            messages.success(request, 'Watchman Profile Created')
            # return render(request, 'watchman/parkzone_watchman_view.html')
            return redirect('watchman_view')
        else:
            messages.error(request, form.errors)
            return render(request, 'watchman/parkzone_watchmancreate.html', {'form': form})
    else:
        print("in else")
        form = Watchman_Form()
        return render(request, 'watchman/parkzone_watchmancreate.html', {'form': form})


@Parkzone_middleware
def watchman_view(request):
    email = request.session.get('email')
    print(email)
    if Watchman.objects.filter(email=email).exists():
        watchman =Watchman.objects.get(email=email)
        query = request.GET.get('watchman')
        if query:
            watchman = Watchman.objects.filter(
                Q(name=query) | Q(city=query)).order_by('-created_at')
        page = request.GET.get('page', 1)
        paginator = Paginator(watchman, 10)
        try:
            watchmans = paginator.page(page)
        except PageNotAnInteger:
            watchmans = paginator.page(1)
        except EmptyPage:
            watchmans = paginator.page(paginator.num_pages)
        return render(request, 'watchman/parkzone_watchman_view.html', {'watchman': watchmans})
    else:
        watchman = Watchman.objects.all()
        return render(request, 'watchman/parkzone_watchman_view.html', {'watchman': watchman})

def watchman_edit(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Watchman.objects.get(id=id)
        form = Watchman_Form(instance=data)
        return render(request, 'watchman/parkzone_watchmanedit.html', {'data': data, 'form': form})
    else:
        return redirect('watchman_view')


def watchman_update(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Watchman.objects.get(id=id)
        form = Watchman_Form(request.POST, request.FILES, instance=data)
        validations = Watchman_Panel_Validations.watchman_validations(form, Watchman, "update")
        if validations == True:
            if form.is_valid():
                form.save()
                messages.success(request, 'Watchman Profile Edited')
                return redirect('watchman_view')
        else:
            messages.error(request, validations)
            return render(request, 'watchman/parkzone_watchmanedit.html', {'data': data, 'form': form})


def watchman_delete(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Watchman.objects.get(id=id)
        data.delete()
        messages.success(request, 'Watchman Profile Deleted')
        return redirect('watchman_view')
    else:
        return redirect('watchman_view')


@Parkzone_middleware
def watchman_payment_record(request):
    print("watchman----pay4")
    society = Society.objects.all()
    if request.method == "POST":
        id = request.POST['society']
        society = Society.objects.filter(id=id)
        watchman = ""
        try:
            watchman = Watchman.objects.filter(society_id=id)
        except:
            print("")
        if watchman:
            return render(request, 'watchman/pz_watchman_payment.html',
                          {'society': society, 'watchman_name': watchman[0].name, 'watchmanid': watchman[0].id})
        else:
            society = Society.objects.all()
            messages.success(request, 'No any watchman found for Society')

            return render(request, "watchman/pz_watchman_payment.html",
                          {'society': society})
    else:
        return render(request, 'watchman/pz_watchman_payment.html', {'society': society})


@Parkzone_middleware
def watchman_salary_payment_record(request):
    print("watchman----pay3",request.POST)
    month = request.POST['month_num']
    print(month,"hiiiiii")
    society = Society.objects.all()
    if request.method == "POST":
        watchmanid = request.POST['watchman']
        if watchmanid:
            watchman = Watchman.objects.get(id=watchmanid)
            name = watchman.name
            watchman_payment_record = Watchman_payment.objects.filter(watchman_id=watchman)
            context = {
                'society': society,
                'watchman_payment_record': watchman_payment_record,
                'is_watchman': 0,
                'watchman_name': name,
                'watchname': name,
                'watchman': watchman,
                'watchmanid': watchmanid,

            }
            return render(request, 'watchman/pz_watchman_payment.html', context)
        else:
            messages.success(request, 'Please Select Wacthman First')
            return redirect("watchman_payment_record")

    else:
        messages.success(request, 'Your Payment Already Done')
        return redirect("watchman_payment_record")


@Parkzone_middleware
def watchman_salary_final_payment(request):
    print("watchman----pay2",request.POST)
    society = Society.objects.all()
    watchman_id = request.POST['watchmanid']
    print(watchman_id)
    if watchman_id:
        month = request.POST['month_num']
        mystr = str(month).split("-")
        month = mystr[1] + "-" + mystr[0]
        selected_date = month + "-01"
        if month:
            watchman = Watchman.objects.get(id=watchman_id)
            print(watchman)
            salary = watchman.salary
            name = watchman.name
            if Watchman_payment.objects.filter(month=selected_date, watchman_id=watchman_id):

                messages.success(request, 'Your Payment Already Done')
                return redirect("watchman_payment_record")
            else:
                print("in else")
                context = {
                    'society': society,
                    'is_watchman': 1,
                    'salary': salary,
                    'watchman_name': name,
                    'name': name,
                    'month_number': selected_date,
                    'watchman_id': watchman_id
                }
                messages.success(request, 'Your Payment Already Done')
                return render(request, 'watchman/pz_watchman_payment.html', context)
        else:
            messages.success(request, 'Please Select Month First')
            return redirect("watchman_payment_record")
    else:
        messages.success(request, 'Please Select Watchman First')
        return redirect("watchman_payment_record")


@Parkzone_middleware
def watchman_salary_history_records(request):
    print("watchman----pay1")
    salary = request.POST['salary']
    month_number = request.POST['month_number']
    watchmanid = request.POST['watchmanid']
    watchman = Watchman.objects.get(id=watchmanid)
    if Watchman_payment.objects.filter(month=month_number, watchman_id=watchmanid):
        messages.success(request, 'Your Payment Is Already Done')
        return redirect("watchman_payment_record")
    else:
        Watchman_payment.objects.create(watchman=watchman, month=month_number, salary=salary, payment_status="Paid")
        messages.success(request, 'Your Payment Is Successfully Done')
        return redirect("watchman_payment_record")

def warchman_view1(request):
    id = request.POST['id']
    watchman = Watchman.objects.filter(id=id)
    array = []
    for x in watchman:
        data = '<div class="row"> <div class="col-md-4"><h4><label>Society Name:</label></h4></div><div class="col-md-8">' + str(x.society) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Name:</label></h4></div><div class="col-md-8">' + str(
            x.name) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>address:</label></h4></div><div class="col-md-8">' + str(
            x.address) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>city:</label></h4></div><div class="col-md-8">' + str(
            x.city) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Mobile Number:</label></h4></div><div class="col-md-8">' + str(
            x.mobile_number) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Email:</label></h4></div><div class="col-md-8">' + str(
            x.email) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>password:</label></h4></div><div class="col-md-8">' + str(
            x.password) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Aadhar Card:</label></h4></div><div class="col-md-8">' + str(
            x.aadhar_card) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Aadhar Number Password:</label></h4></div><div class="col-md-8">' + str(
            x.aadhar_num) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Passport Photo:</label></h4></div><div class="col-md-8">' + str(
            x.passport_photo) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Salary:</label></h4></div><div class="col-md-8">' + str(
            x.salary) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Arrival Time:</label></h4></div><div class="col-md-8">' + str(
            x.arrival_time) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Departure Time</label></h4></div><div class="col-md-8">' + str(
            x.departure_time) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Join Date:</label></h4></div><div class="col-md-8">' + str(
            x.join_date) + '</div></div>'
        array.append(data)
    return HttpResponse(array)
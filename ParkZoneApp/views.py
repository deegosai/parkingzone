from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Society.models import Society, Society_Secretry, Society_Commision_history
from Watchman.middlewares import Parkzone_middleware
from Zone.models import *
from .models import *
from .serializers import AdminSerializer

from django.shortcuts import HttpResponse
from django.db.models import Q
from django.http import JsonResponse
import json
import datetime
from datetime import date
from datetime import timedelta
# Create your views here.
from User.models import User
from Zone.models import *


@api_view(['POST'])
def Admin_Create(request):
    if request.method == 'POST':
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            print("serializer---", serializer)
            serializer.save()
            return Response({"error": "0", "message": "Data created succesfully", "data": serializer.data, })
        else:
            return Response({"error": "1", "message": "Can't create data"})


def adminlogin(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if not (email and password):
            messages.success(request, 'Your Email Or Password Is Null')
            return render(request, 'login.html')
        else:
            if Login.objects.filter(email=email, password=password).exists():
                data = Login.objects.get(email=email, password=password)
                if data.type == "societysecretry":
                    request.session['email'] = email
                    request.session['password'] = password
                    request.session['usertype'] = 'societysecretry'
                    return parkzone_notify(request)
                else:
                    if data.type == "parkingslotowner":
                        request.session['email'] = email
                        request.session['password'] = password
                        request.session['usertype'] = 'parkingslotowner'
                        return parkzone_notify(request)

                    else:
                        messages.success(request, 'Your Email Or Password Is Invalid')
                        return render(request, 'login.html')
            else:
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    request.session['email'] = email
                    request.session['password'] = password
                    request.session['usertype'] = 'admin'
                    return redirect("dashboard")
                else:
                    messages.success(request, 'Your Email Or Password Is Invalid')
                    return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout(request):
    if request.session.get('email'):
        del request.session['email']
        del request.session['password']
        return redirect('adminlogin')
    if not request.session.get('email'):
        return redirect('adminlogin')


def dashboard(request):
    # bulding = Building.objects.count()
    # buldingowner = Building_Owner.objects.count()
    usertype = request.session.get('usertype')
    if request.method=="POST":
        print("******************", request.POST)
        if usertype == "admin":
            if str(request.POST).__contains__("city_selected"):
                print("########## in if")
                selected_city=request.POST['city_selected']

                today=datetime.now().date()
                print(today)
                todayBookings=Zone_Booking.objects.all()#filter(booking_date=today)
                print(todayBookings)
                arr=[]
                city= ""
                ps_count=0
                for booking in todayBookings:
                    print(type(booking.booking_date))
                    print(type(today))
                    if booking.booking_date==today :################################or booking.activated_package_expire > today:
                        print("in for loop----",booking)
                        book_city=booking.park_slot.society.city
                        print(str(book_city).lower()==str(selected_city).lower())
                        if str(book_city).lower().__contains__(selected_city):
                            arr.append(booking.park_slot)
                            city=selected_city
                            ps_count=len(arr)
                return HttpResponse(city+"&"+str(ps_count))
            else:
                print("########## in else")
                ################# city vise last 10 days booking ##########
                print(request.POST, "++++++")
                selected_city = request.POST['city']
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                # today=datetime.datetime.today().date()
                startDate = datetime.strptime(start_date, "%Y-%m-%d")
                endDate= datetime.strptime(end_date, "%Y-%m-%d")
                delta = endDate - startDate

                dict = {}
                for i in range(delta.days + 1):
                    print(i)
                    arr = []
                    mydate=startDate + timedelta(days=i)
                    print(mydate,"-----mydate")
                    dateArr=str(mydate).split(" ")
                    usethisDate=datetime.strptime(dateArr[0], "%Y-%m-%d")
                    print(usethisDate,"-----------use")
                    bookings = Zone_Booking.objects.filter(booking_date=usethisDate)
                    for booking in bookings:
                        book_city = booking.park_slot.society.city
                        if str(book_city).lower().__contains__(selected_city):
                            arr.append(booking.park_slot)
                            dict[str(booking.booking_date)] = len(arr)
                            print("dict------------------>>>>>",dict)
                    print(dateArr[0],bookings)
                print(dict)
                return HttpResponse(json.dumps(dict))


    else:
        global book_details
        society = Society.objects.count()
        user = User.objects.count()
        Parkslot = Park_slot.objects.count()
        booking = Zone_Booking.objects.count()
        zones = Park_slot.objects.count()


        if usertype == "admin":

            ################ user : last 10 days booking #################
            today = datetime.today().date()
            print('today', today)
            var = Zone_Booking.objects.filter(booking_date__range=(today - timedelta(days=10), today))
            print("var--------------",var)
            mydata = {}
            count = 0
            for x in var:
                print("x------------",x)
                if not x.booking_date in mydata.keys():
                    count = 1
                    mydata[x.booking_date] = count
                else:
                    count = count + 1
                    mydata[x.booking_date] = count
            x_axis = []
            y_axis = []
            for key, value in mydata.items():
                y_axis.append(value)
                x_axis.append(str(key))
            print("x_axis",x_axis)
            print("y_axis", y_axis)
            data = Zone_Booking.objects.all()
            dict = {}
            for x in data:
                if not x.activated_package in dict.keys():
                    counter = 0
                    counter = counter + 1
                    dict[x.activated_package] = counter
                else:
                    dict[x.activated_package] = dict[x.activated_package] + 1
            print("x_axis1", x_axis)
            print("y_axis1", y_axis)
            var = Admin_Wallet.objects.all()

            print("var", var)
           ################ city wise slot book count today #################
            societies = Society.objects.all()
            print("@@@@@@@@@@@@@@@@@", societies)
            list = []
            for x in societies:
                if not str(x.city).lower() in list:
                    list.append(str(x.city).lower())
            print("=========>>>", list)
            return render(request, 'index.html',
                          {'a': society, 'b': Parkslot, 'c': user, 'd': booking, 'e': zones, 'x_axis': x_axis,
                           'y_axis': y_axis, 'x_axis1': dict.keys(), 'y_axis1': dict.values(), 'var': var,
                           'city_list': list,'city':list})




        elif usertype == "societysecretry":
            ################ city wise slot book count today #################
            email = request.session.get('email')
            societysecretry = Society_Secretry.objects.get(email=email)
            society = Society.objects.get(id=societysecretry.society_id)

            print("@@@@@@@@@@@@@@@@@", society)
            list = []

            if not str(society.city).lower() in list:
                list.append(str(society.city).lower())
            ################ user : last 10 days booking #################
            email = request.session.get('email')
            societysecretry = Society_Secretry.objects.get(email=email)
            society = Society.objects.get(id=societysecretry.society_id)
            society_payment_record = Society_Commision_history.objects.filter(society_id=society.id)
            if society_payment_record:
                society_amount = society_payment_record[0].amount
                society_amount_date = society_payment_record[0].created_at
                parkslot = Park_slot.objects.filter(society_id=societysecretry.society_id)
                for i in parkslot:
                    parkslot_id = i.id
                    today = datetime.datetime.today().date()
                    book_details = Zone_Booking.objects.filter(park_slot_id=parkslot_id,
                                                               booking_date__range=(
                                                               today - datetime.timedelta(days=10), today))
                    dict = {}
                    for x in book_details:
                        if not x.booking_date in dict.keys():
                            counter = 0
                            counter = counter + 1
                            dict[x.booking_date] = counter
                        else:
                            dict[x.booking_date] = dict[x.booking_date] + 1
                return render(request, "index.html",
                              {'society_amount_date': society_amount_date, 'society_amount': society_amount,
                               'x_axis': dict.keys(), 'y_axis': dict.values(),
                           'city_list': list,'city':list})
            else:
                print("hi")
                dict = {}
                parkslot = Park_slot.objects.filter(society_id=societysecretry.society_id)
                for i in parkslot:
                    parkslot_id = i.id
                    today = datetime.datetime.date.today()
                    book_details = Zone_Booking.objects.filter(park_slot_id=parkslot_id,
                                                               booking_date__range=(
                                                               today - datetime.timedelta(days=10), today))

                    for x in book_details:
                        if not x.booking_date in dict.keys():
                            counter = 0
                            counter = counter + 1
                            dict[x.booking_date] = counter
                        else:
                            dict[x.booking_date] = dict[x.booking_date] + 1

                return render(request, "index.html",
                              {'x_axis': dict.keys(), 'y_axis': dict.values(),
                           'city_list': list,'city':list})

        elif usertype == "parkingslotowner":
            ################ city wise slot book count today #################
            email = request.session.get('email')
            parkslotowner = Park_Slot_Owner.objects.get(email=email)

            society = Society.objects.get(id=parkslotowner.park_slot.society.id)

            print("@@@@@@@@@@@@@@@@@", society)
            list = []

            if not str(society.city).lower() in list:
                list.append(str(society.city).lower())
            ################ user : last 10 days booking #################
            email = request.session.get('email')
            parkingslotowner = Park_Slot_Owner.objects.get(email=email)
            parkingslot = Park_Slot_Owner_Commision_history.objects.filter(park_slot_owner_id=parkingslotowner.id)
            if parkingslot:
                parkingslotowneramount = parkingslot[0].amount
                parkingslotamountdate = parkingslot[0].created_at
                print(parkingslotowneramount)
                parkslot = Park_slot.objects.filter(society_id=parkingslotowner.park_slot_id)
                for i in parkslot:
                    parkslot_id = i.id
                    today = datetime.datetime.today().date()
                    book_details = Zone_Booking.objects.filter(park_slot_id=parkslot_id,

                                                               booking_date__range=(
                                                               today - datetime.timedelta(days=10), today))
                dict = {}
                for x in book_details:
                    if not x.booking_date in dict.keys():
                        counter = 0
                        counter = counter + 1
                        dict[x.booking_date] = counter
                        print(dict)
                    else:
                        dict[x.booking_date] = dict[x.booking_date] + 1
                return render(request, "index.html", {'parkingslotamountdate': parkingslotamountdate,
                                                      'parkingslotowneramount': parkingslotowneramount,
                                                      'x_axis': dict.keys(), 'y_axis': dict.values(),
                           'city_list': list,'city':list})
            else:
                print("hi")
                parkslot = Park_slot.objects.filter(society_id=parkingslotowner.park_slot_id)
                dict = {}
                for i in parkslot:
                    parkslot_id = i.id
                    today = datetime.datetime.today().date()
                    book_details = Zone_Booking.objects.filter(park_slot_id=parkslot_id,
                                                               booking_date__range=(
                                                               today - datetime.timedelta(days=10), today))

                    for x in book_details:
                        if not x.booking_date in dict.keys():
                            counter = 0
                            counter = counter + 1
                            dict[x.booking_date] = counter
                        else:
                            dict[x.booking_date] = dict[x.booking_date] + 1
                return render(request, "index.html",
                              {'x_axis': dict.keys(), 'y_axis': dict.values(),
                           'city_list': list,'city':list})


@Parkzone_middleware
def pz_Admin_view(request):
    mysoc = Admin.objects.all()
    context = {
        'dictionary': mysoc,
    }
    return render(request, "society/parkzone_society.html", context)


@Parkzone_middleware
def society_and_admin_payment_report(request):
    if request.method == "POST":
        email = request.session.get('email')
        print(request.POST, "--------")
        society = Society.objects.all()
        soc_id = request.POST['society']

        month = request.POST['month']
        print(month)
        if month:
            mystr = str(month).split("-")
            month = mystr[1] + "-" + mystr[0]
            selected_date = month + "-01"
            print(selected_date)
            selected_society = Society.objects.get(id=soc_id)
            print(selected_society.city)
            Soc_Commision_history = ""
            try:
                Soc_Commision_history = Society_Commision_history.objects.get(society=selected_society,
                                                                              month=selected_date)
                print("obj che")
            except:
                print("in exception")
            flag = ""
            objs = Park_slot.objects.filter(society=selected_society.id)
            print("objs----", objs)
            for x in objs:
                bookingObjs = Zone_Booking.objects.filter(park_slot=x.id)
                for x in bookingObjs:
                    print("in inner for")
                    if x.park_slot.society.name == selected_society.name:
                        bookdate = x.booking_date
                        arr = str(bookdate).split("-")
                        mydate = arr[0] + "-" + arr[1]
                        print(mydate)
                        if str(mydate) == str(month):
                            flag = "has_bookings"

            if Soc_Commision_history:

                if Soc_Commision_history and Soc_Commision_history.payment_status.lower() == 'paid':

                    context = {'soc': soc_id, 'name': selected_society.name, 'society': society,
                               'data': Soc_Commision_history}
                    return render(request, 'parkzoneapp/parkzone_society_payment_report.html', context)
                elif flag == "has_bookings" and Soc_Commision_history.payment_status.lower() == 'due':
                    total = Soc_Commision_history.commision_due_amount
                    context = {'soc': soc_id, 'name': selected_society.name, 'selected_society': selected_society,
                               'selected_month': month, 'society': society,
                               'amount': total, 'isDue': 'True'}
                    return render(request, 'parkzoneapp/parkzone_society_payment_report.html', context)

            elif flag == "has_bookings":
                montharr = str(month).split("-")
                start_date = month + str("-01")
                # end_date = month + str("-31")
                if montharr[1] == '02':
                    end_date = month + str("-29")
                if montharr[1] == '04' or montharr[1] == '06' or montharr[1] == '09' or montharr[1] == '11':
                    end_date = month + str("-30")
                else:
                    end_date = month + str("-31")
                x = Zone_Booking.objects.filter(booking_date__range=[start_date, end_date])
                print(x, "----x")
                total = 0
                for y in x:
                    total = total + y.booking_amount
                print(total, "total", selected_society.commision)
                soc_Commision = (total * selected_society.commision) / 100

                print(soc_Commision, "soc_Commision")
                context = {'soc': soc_id, 'name': selected_society.name, 'selected_society': selected_society,
                           'selected_month': month, 'society': society,
                           'amount': soc_Commision, 'total_booking_amount': total}
                return render(request, 'parkzoneapp/parkzone_society_payment_report.html', context)
            else:
                print("in else")
                society = Society.objects.all()
                return render(request, 'parkzoneapp/parkzone_society_payment_report.html',
                              {'society': society, 'message': 'No bookings available'})
        else:
            messages.error(request, "please select month")
            society = Society.objects.all()
            return render(request, 'parkzoneapp/parkzone_society_payment_report.html',
                          {'society': society, 'message': 'please select month'})
    else:
        email = request.session.get('email')
        print("--------in get----------", email)
        if Society_Secretry.objects.filter(email=email).exists():
            ss = Society_Secretry.objects.get(email=email)
            soc_obj = ss.society
            return render(request, 'parkzoneapp/parkzone_society_payment_report.html',
                          {'soc': soc_obj, "name": soc_obj.name})
        else:
            society = Society.objects.all()
            return render(request, 'parkzoneapp/parkzone_society_payment_report.html', {'society': society})


def save_soc_Payment(request):
    if request.method == "POST":
        print(request.POST)
        payAmt = request.POST['paidamount']
        print(payAmt)
        dueAmt = request.POST['dueamount']

        print(dueAmt, "due")
        total_booking_amt = request.POST['total_booking_amount']
        Amount = request.POST['amt_']
        soc_id = request.POST['society']
        selected_society = Society.objects.get(id=soc_id)
        month = request.POST['selected_month']
        date = str(month) + "-01"
        if str(dueAmt).strip() == '0':
            print("in if", dueAmt)
            status = 'paid'
        else:
            print("in else", dueAmt)
            status = 'due'
        soc_commision_history = Society_Commision_history(society=selected_society, month=date, payment_status=status,
                                                          amount=Amount, commision_paid_amount=payAmt,
                                                          commision_due_amount=dueAmt)
        soc_commision_history.save()
        admin_Commision = (float(total_booking_amt) * float(100 - selected_society.commision)) / 100
        AdminWallet = Admin_Wallet(society=selected_society, month=date, payment_status="1",
                                   amount=admin_Commision,
                                   commision_paid_amount=admin_Commision, commision_due_amount=0.0)
        AdminWallet.save()

        date=datetime.today().date()
        time=datetime.today().time()
        notify=Notification(message="Admin credited "+str(Amount)+" amount for  "+" month " +month,
        message_owner="SS",message_date=date,message_time=time,is_read=False)
        notify.save()
    society = Society.objects.all()
    return render(request, 'parkzoneapp/parkzone_society_payment_report.html', {'society': society})


def update_soc_Payment(request):
    if request.method == "POST":
        payAmt = request.POST['paidamount']
        dueAmt = request.POST['dueamount']
        print(dueAmt, "due")
        Amount = request.POST['amt_']
        print(Amount, "amt")
        soc_id = request.POST['society']
        if float(dueAmt) < 0:
            messages.error("You can not pay more than booking amount")
        else:
            print(soc_id)
            selected_society = Society.objects.get(id=soc_id)
            month = request.POST['selected_month']
            date = str(month) + "-01"
            print(date)
            if str(dueAmt).strip() == '0':
                print("in if", dueAmt)
                status = 'paid'
            else:
                print("in else", dueAmt)
                status = 'due'

            soc_commision_history = Society_Commision_history.objects.get(society=selected_society,month=date)

            soc_commision_history.commision_paid_amount = payAmt
            soc_commision_history.commision_due_amount = dueAmt
            # soc_commision_history.amount = Amount
            soc_commision_history.payment_status = status
            soc_commision_history.save()
            date = datetime.today().date()
            time = datetime.today().time()
            notify = Notification(message="Admin credited " + str(Amount) + " amount for  " + " month " + month,
                                  message_owner="SS", message_date=date, message_time=time, is_read=False)
            notify.save()

    society = Society.objects.all()
    return redirect('society_and_admin_payment_report', {'society': society})


@Parkzone_middleware
def society_payment_record(request):
    Soc_Commision_history = Society_Commision_history.objects.all()
    query = request.GET.get('Soc_Commision_history')
    if query:
        Soc_Commision_history = Society_Commision_history.objects.filter(
            Q(amount=query)).order_by('id')
    page = request.GET.get('page', 1)
    paginator = Paginator(Soc_Commision_history, 10)
    try:
        Soc_Commision_history = paginator.page(page)
    except PageNotAnInteger:
        Soc_Commision_history = paginator.page(1)
    except EmptyPage:
        Soc_Commision_history = paginator.page(paginator.num_pages)
    return render(request, 'parkzoneapp/pz_society_report.html', {'Soc_Commision_history': Soc_Commision_history})

@Parkzone_middleware
def parkingslotowner_and_admin_payment_report(request):
    if request.method == "POST":
        print(request.POST)
        pso = request.POST['pso']

        month = request.POST['month']
        if month:
            print(month)
            mystr = str(month).split("-")
            month = mystr[1] + "-" + mystr[0]
            selected_date = month + "-01"
            print(selected_date)
            selected_slot_owner = Park_Slot_Owner.objects.get(id=pso)
            name = selected_slot_owner.name
            flag = ""
            ps_owner_Commision_history = ""
            try:
                ps_owner_Commision_history = Park_Slot_Owner_Commision_history.objects.get(
                    park_slot_owner=selected_slot_owner, month=selected_date)
                print("obj che")
            except:
                print("in exception")
            park_slot = selected_slot_owner.park_slot

            bookingObjs = Zone_Booking.objects.filter(park_slot=park_slot.id)
            for x in bookingObjs:

                bookdate = x.booking_date
                arr = str(bookdate).split("-")
                mydate = arr[0] + "-" + arr[1]
                print(mydate, "----mydate")
                print(month, "---month")
                if str(mydate) == str(month):
                    flag = "has_bookings"
            if ps_owner_Commision_history:
                if ps_owner_Commision_history and ps_owner_Commision_history.payment_status.lower() == 'paid':
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@------paid")
                    context = {'pso': pso, 'name': name, 'month': month, 'data': ps_owner_Commision_history}
                    return render(request, 'ParkSlotOwner/pz_parkslot_owner_payment_make.html', context)
                elif flag == "has_bookings" and ps_owner_Commision_history.payment_status.lower() == 'due':
                    print("due")
                    total = ps_owner_Commision_history.commision_due_amount
                    print(selected_slot_owner, "#####")
                    context = {'pso': pso, 'name': name, 'month': month, 'slot': park_slot,
                               'amount': total, 'isDue': 'True'}
                    return render(request, 'ParkSlotOwner/pz_parkslot_owner_payment_make.html', context)
            if flag == "has_bookings":
                montharr = str(month).split("-")
                start_date = month + str("-01")
                # end_date = month + str("-31")
                if montharr[1] == '02':
                    end_date = month + str("-29")
                if montharr[1] == '04' or montharr[1] == '06' or montharr[1] == '09' or montharr[1] == '11':
                    end_date = month + str("-30")
                else:
                    end_date = month + str("-31")
                x = Zone_Booking.objects.filter(booking_date__range=[start_date, end_date])
                print(x, "----x")
                total = 0
                for y in x:
                    total = total + y.booking_amount

                soc_Commision = (total * selected_slot_owner.commision) / 100
                print(soc_Commision, "soc_Commision")
                context = {'selected_park_slot_owner': selected_slot_owner, 'selected_month': month,
                           'amount': soc_Commision, 'pso': pso, 'name': name, 'total_booking_amount': total}
                return render(request, 'ParkSlotOwner/pz_parkslot_owner_payment_make.html', context)
            else:
                print("in else")
                Park_Slot_Owners = Park_Slot_Owner.objects.all()
                return render(request, 'ParkSlotOwner/pz_parkslot_owner_payment_make.html',
                              {'Park_Slot_Owner': Park_Slot_Owners, 'message': 'No bookings available'})
        else:
            messages.error(request, "please select month")
            Park_Slot_Owners = Park_Slot_Owner.objects.all()
            return render(request, 'ParkSlotOwner/pz_parkslot_owner_payment_make.html',
                          {'Park_Slot_Owner': Park_Slot_Owners, 'message': 'Please select month'})
    else:
        email = request.session.get('email')
        print("--------in get----------", email)
        if Society_Secretry.objects.filter(email=email).exists():
            ss = Society_Secretry.objects.get(email=email)
            soc_obj = ss.society

            return render(request, 'parkzoneapp/parkzone_society_payment_report.html',
                          {'soc': soc_obj, "name": soc_obj.name})
        else:
            Park_Slot_Owners = Park_Slot_Owner.objects.all()
            return render(request, 'ParkSlotOwner/pz_parkslot_owner_payment_make.html',
                          {'Park_Slot_Owner': Park_Slot_Owners})


def parkslot_owner_payment_record(request):
    park_slot_owner_Commision_history = Park_Slot_Owner_Commision_history.objects.all()
    query = request.GET.get('park_slot_owner_Commision_history')
    # park_slot_owner_Commision_history=Park_Slot_Owner_Commision_history()
    if query:
        park_slot_owner_Commision_history = Park_Slot_Owner_Commision_history.objects.filter(
            Q(amount=query)).order_by('id')
        # print(park_slot_owner_Commision_history)
    page = request.GET.get('page', 1)
    paginator = Paginator(park_slot_owner_Commision_history, 10)
    try:
        park_slot_owner_Commision_history = paginator.page(page)
    except PageNotAnInteger:
        park_slot_owner_Commision_history = paginator.page(1)
    except EmptyPage:
        park_slot_owner_Commision_history = paginator.page(paginator.num_pages)
    # print(park_slot_owner_Commision_history)
    return render(request, 'parkzoneapp/pz_parkslot_owner_payment_report.html',
                  {'park_slot_owner_commision_history': park_slot_owner_Commision_history})


def save_ps_owner_Payment(request):
    if request.method == "POST":
        print(request.POST)
        payAmt = request.POST['paidamount']
        print(payAmt)
        dueAmt = request.POST['dueamount']
        print(dueAmt, "due")
        Amount = request.POST['amt_']
        po_id = request.POST['selected_ps_owner']
        owner = Park_Slot_Owner.objects.get(id=po_id)

        selected_soc = owner.park_slot.society
        month = request.POST['selected_month']
        date = str(month) + "-01"
        if str(dueAmt).strip() == '0':
            print("in if", dueAmt)
            status = 'paid'
        else:
            print("in else", dueAmt)
            status = 'due'
        history = Park_Slot_Owner_Commision_history(park_slot_owner=owner, month=date, payment_status=status,
                                                    amount=Amount, commision_paid_amount=payAmt,
                                                    commision_due_amount=dueAmt)
        history.save()
        date = datetime.today().date()
        time = datetime.today().time()
        notify = Notification(message="Admin credited " + str(Amount) + " amount for  " + " month " + month,
                              message_owner="PO", message_date=date, message_time=time, is_read=False)
        notify.save()

    parkingslotowner = Park_Slot_Owner.objects.all()
    return redirect("parkingslotowner_and_admin_payment_report")


def update_park_slot_owner_Payment(request):
    if request.method == "POST":
        print("#############", request.POST)
        payAmt = request.POST['paidamount']
        dueAmt = request.POST['dueamount']
        print(dueAmt, "due")
        Amount = request.POST['amt_']
        print(Amount, "amt")
        pso = request.POST['selected_ps_owner']

        print(pso)
        selected_po = Park_Slot_Owner.objects.get(id=pso)
        month = request.POST['selected_month']
        date = str(month) + "-01"
        print(date)
        if str(dueAmt).strip() == '0':
            print("in if", dueAmt)
            status = 'paid'
        else:
            print("in else", dueAmt)
            status = 'due'
        parking_slot_owner_commision_history = Park_Slot_Owner_Commision_history.objects.get(
            park_slot_owner=selected_po,month=date)
        parking_slot_owner_commision_history.commision_paid_amount = payAmt
        parking_slot_owner_commision_history.commision_due_amount = dueAmt
        parking_slot_owner_commision_history.payment_status = status
        parking_slot_owner_commision_history.save()
        date = datetime.today().date()
        time = datetime.today().time()
        notify = Notification(message="Admin credited " + str(Amount) + " amount for  " + " month " + month,
                              message_owner="PO", message_date=date, message_time=time, is_read=False)
        notify.save()

    parkingslotowner = Park_Slot_Owner.objects.all()
    return redirect("parkingslotowner_and_admin_payment_report")

def parkzone_notify(request):

    email = request.session.get('email')
    if Society_Secretry.objects.filter(email=email).exists():
        ss = Society_Secretry.objects.get(email=email)
        print(ss,"=====")
        ss_notify=Notification.objects.filter(message_owner="SS")
        print(ss_notify,"hiii")
        count=Notification.objects.filter(message_owner="SS",is_read=False).count()
        context={
            'ss_notify':ss_notify,
            'count':count,
        }
        return render(request,"index.html",context)
    elif Park_Slot_Owner.objects.filter(email=email).exists():
        po = Park_Slot_Owner.objects.get(email=email)
        print(po,"=====")
        po_notify=Notification.objects.filter(message_owner="PO")
        print(po_notify,"hiii")
        count=Notification.objects.filter(message_owner="PO",is_read=False).count()
        context={
            'po_notify':po_notify,
            'count':count,
        }
        return render(request,"index.html",context)


def parkzone_notify_change(request):
    if request.method=="POST":
        id=request.POST['id']
        print(id)
        notifyOBJ=Notification.objects.get(id=id)
        notifyOBJ.is_read=True
        notifyOBJ.save()
        return HttpResponse(id)

def notifaction_detail(request):
    email = request.session.get('email')
    if Society_Secretry.objects.filter(email=email).exists():

        ss_notify = Notification.objects.filter(message_owner="SS")


        context = {
            'notify': ss_notify,

        }
        return render(request, "parkzoneapp/notifaction_detail.html", context)
    elif Park_Slot_Owner.objects.filter(email=email).exists():

        po_notify = Notification.objects.filter(message_owner="PO")
        print(po_notify, "hiii")

        context = {
            'notify': po_notify,

        }
        return render(request, "parkzoneapp/notifaction_detail.html", context)

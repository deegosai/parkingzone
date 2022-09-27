from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from xlwt import Workbook
from Zone.forms import *
from ParkZoneApp.models import *
from Watchman.middlewares import Parkzone_middleware
from Zone.models import *
from . import Society_Panel_Validations
from .forms import Society_Form, SocietySecretry_Form
from .models import Society_Commision_history
from .serializers import *
from django.db.models import Q
from .models import *
# Create your views here.
import pandas as pd
from Watchman.models import Watchman

from ParkZoneApp.models import Admin_Deal

from ParkZoneApp.models import Login
import math
from math import radians, cos, sin, asin, sqrt
from django.http import HttpResponse


# from Zone.models import Booking
from django.shortcuts import render

@api_view(['POST'])
def search_societies(request):
    if request.method == 'POST':
        lat = request.POST['lat']
        long = request.POST['long']
        all_Soc = Society.objects.all()
        print(str(all_Soc))
        arr = []

        i = 0
        for soc in all_Soc:
            dict = {}
            print(soc.name, "---soc")
            soc_long = soc.longtitude,
            soc_late = soc.langtitude,
            soc_long = float(soc_long[0])
            soc_late = float(soc_late[0])
            lat = float(lat)
            long = float(long)
            print(soc_long, "---lat")
            print(soc_late, "---long")
            print("-------------------------")
            # convert decimal degrees to radians
            lon1, lat1, lon2, lat2 = map(radians, [soc_long, soc_late, long, lat])
            print(lon1, "@@@@@@@@")
            # haversine formula
            dlon = lon2 - lon1
            dlat = lat2 - lat1
            print(dlon, "@@@@@@@@")
            a = float(sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2)
            c = 2 * asin(sqrt(a))
            r = 6371  # Radius of earth in kilometers. Use 3956 for miles
            km = r * c
            print(km)
            if km < 1.0:
                dict["id"] = soc.id
                dict["name"] = soc.name
                dict["long"] = soc.longtitude
                dict["lat"] = soc.langtitude
                arr.append(dict)
            i = i + 1
        print("HRERE GOT ",arr)
        if len(arr) == 0:
            return Response({"error": "1", "message": "Societies are not visible", "data": []})
        else:
            return Response({"error": "0", "message ": "Societies are visible", "data": arr})


@api_view(['POST'])
def society_Create(request):
    if request.method == 'POST':
        serializer = SocietySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"error": "0", "message ": "Data created succesfully", "data": serializer.data, })
        else:
            return Response({"error": "1", "message": "Can't create data"})


@api_view(['POST'])
def society_Update(request):
    pk = request.POST['id']
    soc = Society.objects.get(id=pk)
    print("pk=", pk)
    serializer = SocietySerializer(instance=soc, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"error": "0", "message ": "Data Updated", "data": serializer.data, })
    else:
        return Response({"error": "1", "message": "Data Not updated"})


@api_view(['POST', 'DELETE'])
def society_Delete(request):
    pk = request.POST['id']
    soc = Society.objects.get(id=pk)
    if soc:
        soc.delete()
        return Response({"error": "0", "message ": "Data Deleted"})
    else:
        return Response({"error": "1", "message": "Data not deleted"})


@api_view(['POST'])
def society_detail_view(request):
    pk = request.POST['society_id']
    soc = Society.objects.filter(id=pk).values()
    if soc:
        return Response({"error": "0", "message ": "Society is visible", "data": soc, })
    else:
        return Response({"error": "1", "message": "Society is not visible"})


@api_view(['POST', 'GET'])
def SocietysecretryRegister(request):
    if request.method == "POST":
        serializer = Societysecretry_Serializer(data=request.data)
        if serializer.is_valid():

            serializer.save()

            return Response({"error": "0", "message ": "Data Created", "data": request.data})
        else:
            return Response({"error": "1", "message": "please fill all data"})
    else:
        tasks = Society_Secretry.objects.all()
        serializer = Societysecretry_Serializer(tasks, many=True)
        if serializer:
            return Response({"error": "0", "message ": "Your all data", "data": serializer.data, })
        else:
            return Response({"error": "1", "message": "can't find all data"})


@api_view(['POST'])
def SocietysecretryUpdate(request):
    id = request.data['id']
    if not id:
        return Response({"error": "2", "message": "Your ID is NULL"})
    else:
        if Society_Secretry.objects.filter(id=id).exists():
            tasks = Society_Secretry.objects.get(id=id)
            serializer = Societysecretry_Serializer(instance=tasks, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"error": "0", "message ": "Data Updated", "data": serializer.data, })
            else:
                return Response({"error": "1", "message": "Your Data Is Not Updated"})
        else:
            return Response({"error": "2", "message": "data not Available"})


@api_view(['DELETE'])
def SocietysecretryDelete(request):
    if request.method == "DELETE":
        id = request.POST['id']
        if not id:
            return Response({"error": "2", "message": "Your ID is NULL"})
        else:
            if Society_Secretry.objects.filter(id=id).exists():
                tasks = Society_Secretry.objects.get(id=id)
                if tasks:
                    tasks.delete()
                    return Response({"error": "0", "message ": "Data Deleted"})
                else:
                    return Response({"error": "1", "message": "Data Not deleted"})
            else:
                return Response({"error": "2", "message": "Dat Not Available"})


########################################__admin_panel__##################################################


@Parkzone_middleware
def pz_society_view(request):
    print("###############################")
    mysoc = Society.objects.all()
    return render(request, "society/parkzone_society.html", {'mysoc': mysoc,'view_tab':'open','view_style':'display: block;','is_active_view1':'active'})


def pz_society_create(request):
    if request.method == 'POST':
        form = Society_Form(request.POST, request.FILES)

        validations = Society_Panel_Validations.soc_validations(form, Society, "create")
        if validations == True:
            if form.is_valid():
                savedObj = form.save()
                # has_building = form['has_building'].value()
                query = Admin_Deal(society=savedObj, commision=(100 - (savedObj.commision)))
                query.save()
                # if has_building == False:
                #     bform = BuildingForm(request.POST)
                #     return render(request, 'Building/parkzone_building_create.html', {'form': bform,'societyname':savedObj})
                # else:
                return redirect('pz_society_view')
            else:
                messages.error(request, form.errors)
        else:
            messages.error(request, validations)
            return render(request, 'society/parkzone_society_create.html', {'form': form,'view_tab':'open','view_style':'display: block;','is_active_view2':'active'})
    else:
        form = Society_Form()
    return render(request, 'society/parkzone_society_create.html', {'form': form,'view_tab':'open','view_style':'display: block;','is_active_view2':'active'})


def pz_society_edit(request):
    if request.method == "POST":
        id = request.POST['socid']
        soc = Society.objects.get(id=id)
        form = Society_Form(instance=soc)
        return render(request, 'society/parkzone_society_update.html', {'Society': soc, 'form': form})
    else:
        return redirect('pz_society_view')


def pz_society_update(request):
    if request.method == "POST":
        id = request.POST['socid']
        soc = Society.objects.get(id=id)
        form = Society_Form(request.POST, request.FILES, instance=soc)

        if form.is_valid():
            form.save()
            messages.success(request, 'Society Updated Successfully')
            return redirect('pz_society_view')
        else:
            print()
            messages.error(request, form.errors)
            return redirect('pz_society_view')

    else:
        return redirect('pz_society_view')


def pz_society_delete(request):
    if request.method == "POST":
        pk = request.POST['id']
        soc = Society.objects.get(id=pk)

        soc.delete()

        messages.success(request, 'Society Deleted Successfully')
        return redirect('pz_society_view')
    else:
        return redirect('pz_society_view')


@Parkzone_middleware
def Societysecretry_create(request):
    form = SocietySecretry_Form()
    if request.method == "POST":
        form = SocietySecretry_Form(request.POST, request.FILES)
        validations = Society_Panel_Validations.soc_secretry_validations(form, Society_Secretry, "create")
        if validations == True:
            if form.is_valid():
                form.save()
                object = Society_Secretry.objects.last()
                objectid = object.id
                query = Login(number=objectid, email=form['email'].value(), password=form['password'].value(),
                              type='societysecretry')
                query.save()
                messages.success(request, 'Society Secretry Profile Created Successfully')
                return redirect('Societysecretry_view')
            else:
                messages.error(request, form.errors)
        else:
            messages.error(request, validations)
    return render(request, 'society/parkzone_societysecretrycreate.html', {'form': form,'view_tab':'open','view_style':'display: block;','is_active_view4':'active'})


@Parkzone_middleware
def Societysecretry_view(request):
    mysoc = Society_Secretry.objects.all()
    query = request.GET.get('mysoc')
    if query:
        mysoc = Society_Secretry.objects.filter(
            Q(name=query) | Q(city=query) |
            Q(mobile_number=query) | Q(email=query)).order_by('-id')
    print(mysoc)
    if list(mysoc) != []:
        page = request.GET.get('page', 1)
        paginator = Paginator(mysoc, 10)
        try:
            mysocs = paginator.page(page)
        except PageNotAnInteger:
            mysocs = paginator.page(1)
        except EmptyPage:
            mysocs = paginator.page(paginator.num_pages)
        return render(request, 'society/parkzone_societysecretry_view.html', {'mysoc': mysoc,'view_tab':'open','view_style':'display: block;','is_active_view3':'active'})
    else:
        return render(request, 'society/parkzone_societysecretry_view.html', {'mysoc': mysoc,'view_tab':'open','view_style':'display: block;','is_active_view3':'active'})


def Societysecretry_edit(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Society_Secretry.objects.get(id=id)
        form = SocietySecretry_Form(instance=data)
        return render(request, 'society/parkzone_societysecretryedit.html', {'data': data, 'form': form})
    else:
        return redirect('Societysecretry_view')


def Societysecretry_update(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Society_Secretry.objects.get(id=id)
        form = SocietySecretry_Form(request.POST, request.FILES, instance=data)
        validations = Society_Panel_Validations.soc_secretry_validations(form, Society_Secretry, "update")
        if validations == True:
            if form.is_valid():
                obj = form.save()
                print("-------------->>>>", obj.id)
                print(Login.objects.all())
                loginupdate = Login.objects.get(number=obj.id)
                loginupdate.email = form['email'].value()
                loginupdate.password = form['password'].value()
                loginupdate.save()
                messages.success(request, 'Society Secretry Profile Edited Successfully')
                return redirect('Societysecretry_view')
            else:
                messages.error(request, validations)
                return render(request, 'society/parkzone_societysecretryedit.html', {'data': data, 'form': form})
        else:
            messages.error(request, validations)
            return render(request, 'society/parkzone_societysecretryedit.html', {'data': data, 'form': form})


def Societysecretry_delete(request):
    if request.method == "POST":
        id = request.POST['userid']
        data = Society_Secretry.objects.get(id=id)
        login = Login.objects.get(number=data.id)
        data.delete()
        login.delete()
        messages.success(request, 'Society Secretry Profile Profile Deleted Successfully')
        return redirect('Societysecretry_view')
    else:
        return redirect('Societysecretry_view')


def pz_society_billing(request):
    if request.method == "POST":
        print(request.method)
        month = request.POST["month"]
        print("month", month)
        mystr = str(month).split("-")
        month = mystr[1] + "-" + mystr[0]
        # montharr = str(month).split("-")
        print(mystr)
        start_date = month + str("-01")
        end_date = ""
        if mystr[0] == '02':
            end_date = month + str("-29")
        if mystr[0] == '04' or mystr[0] == '06' or mystr[0] == '09' or mystr[0] == '11':
            end_date = month + str("-30")
        else:
            end_date = month + str("-31")
        print("start_date--", start_date)
        print("end_date--", end_date)
        x = Zone_Booking.objects.filter(booking_date__range=[start_date, end_date])
        print(x, "----x")

        dict = {}
        abc = {}
        totalDict = {}
        xyz = {}
        total = 0
        data = {}
        if x:
            wb = Workbook()
            # add_sheet is used to create sheet.
            sheet1 = wb.add_sheet('Sheet 1')
            sheet1.write(0, 0, "Name Of Account Holder")
            sheet1.write(0, 1, "Account Number")
            sheet1.write(0, 2, "Bank Name")
            sheet1.write(0, 3, "IFSC Code")
            sheet1.write(0, 4, "Branch")
            sheet1.write(0, 5, "Month")
            sheet1.write(0, 6, "Amount")
            i = 1
            soc_total = 0
            for y in x:
                acc_holder_name = y.park_slot.society.name
                print("y--->", y, "--------->", acc_holder_name)
                total = total + y.booking_amount
                if not acc_holder_name in dict.keys():

                    totalDict[acc_holder_name] = y.booking_amount
                    print("@@@@@@@@@@@@", totalDict[acc_holder_name], "@@@@@@@@@@", y.booking_amount)
                    dict[acc_holder_name] = y
                    print("in if-----", totalDict)
                elif acc_holder_name in dict.keys():

                    totalDict[acc_holder_name] = totalDict[acc_holder_name] + y.booking_amount
                    print("#############", totalDict[acc_holder_name], "###########", y.booking_amount)
                    dict[acc_holder_name] = y

                    print("in elif-----", dict)
            print(dict)
            k = 0
            data_list = []
            for y in dict.values():
                j = 0
                data = {}
                acc_holder_name = y.park_slot.society.name
                account_Num = y.park_slot.society.account_number
                bank_Name = y.park_slot.society.bank_name
                ifsc_code = y.park_slot.society.ifsc_code
                branch = y.park_slot.society.branch
                booking_amount = totalDict[acc_holder_name]
                data['acc_holder_name'] = acc_holder_name
                data['account_Num'] = account_Num
                data['bank_name'] = bank_Name
                data['ifsc_code'] = ifsc_code
                data['branch'] = branch
                data['booking_amount'] = booking_amount
                data_list.append(data)
                k = k + 1
                sheet1.write(i, j, acc_holder_name)
                j = j + 1
                sheet1.write(i, j, account_Num)
                j = j + 1
                sheet1.write(i, j, bank_Name)
                j = j + 1
                sheet1.write(i, j, ifsc_code)
                j = j + 1
                sheet1.write(i, j, branch)
                j = j + 1
                sheet1.write(i, j, month)
                j=j+1
                sheet1.write(i, j, booking_amount)
                i = i + 1

            sheet1.write(i, j, total)

            xlspath = 'media/Reports/commision.xls'
            wb.save(xlspath)
            print("data", data_list)
            context = {
                'summary_data': data_list,
                'total': total,
                'month': start_date,
                'display_month':month,
            }

            return render(request, 'society/parkzone_society_billing_report.html', context)
        else:

            return render(request, 'society/parkzone_society_billing_report.html',
                          {'message': 'Billing already done for this month'})


    else:
        if Society.objects.count() > 0:
            data = Society.objects.all()
            return render(request, 'society/parkzone_society_billing_report.html', {
                'form': data,
            })
        else:
            return render(request, 'society/parkzone_society_billing_report.html')


def some_view(request):
    response = HttpResponse(content_type='text/csv')
    response = FileResponse(open('media/Reports/commision.xls', 'rb'))
    return response


@Parkzone_middleware
def pz_society_detail(request):
    email = request.session.get('email')
    data = Society_Secretry.objects.get(email=email)
    society = Society.objects.get(id=data.society_id)
    return render(request, 'society/parkzone_society_detail.html', {'society': society})


@Parkzone_middleware
def pz_society_detail_edit(request):
    id = request.POST['socid']
    if request.method == "POST":
        data = Society.objects.get(id=id)
        form = Society_Form(instance=data)
        return render(request, 'society/parkzone_society_detail_update.html', {'Society': data, 'form': form})
    else:
        return redirect('pz_society_detail')


def pz_society_detail_update(request):
    if request.method == "POST":
        id = request.POST['socid']
        data = Society.objects.get(id=id)
        form = Society_Form(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Society Details  Edited')
            return redirect('pz_society_detail')
        else:
            messages.success(request, 'Society Details Are Invalid')
            return redirect('pz_society_detail')
    else:
        return redirect('pz_society_detail')


def society_report(request):
    if request.method == "POST":
        userid = request.POST['society']
        start_date = request.POST['start_date']
        # end_date = request.POST['last_date']
        print(start_date)
        societyid = request.POST['societyid']
        if start_date:
            societysecretry_detail = Society_Secretry.objects.get(id=userid)
            societydetails = Society.objects.get(id=societysecretry_detail.society_id)
            # if societysecretry_detail.society_id in Society_Secretry_Commision_history.objects.all():
            societyhistory = Society_Commision_history.objects.get(
                society_id=societysecretry_detail.society_id)
            print("societyhistory", societyhistory)
            SocietySecretry = Society_Secretry.objects.all()
            context = {
                'societysecretry': societysecretry_detail,
                'societydetails': societydetails,
                'societyhistory': societyhistory,
                'society': SocietySecretry,
                'start_date': start_date,
                # 'end_date': end_date
            }
            return render(request, 'society/pz_society_report.html', context)

        else:
            messages.success(request, "invalid date")
            SocietySecretry = Society_Secretry.objects.all()
            return render(request, 'society/pz_society_report.html',
                          {'society': SocietySecretry, 'start_date': start_date})

    else:
        SocietySecretry = Society_Secretry.objects.all()
        return render(request, 'society/pz_society_report.html', {'society': SocietySecretry})


def watchaman_records(request):
    email = request.session.get('email')
    print(email)
    ss_record = Society_Secretry.objects.get(email=email)
    society_record = Society.objects.filter(id=ss_record.society_id)
    if society_record:
        data = []
        for brecord in society_record:
            id = brecord.id
            data.append(id)
        for wdata in data:
            watchmanrecord = Watchman.objects.filter(society_id=wdata)
            if watchmanrecord:
                query = request.GET.get('watchamanrecord')
                if query:
                    watchamanrecord = Watchman.objects.filter(
                        Q(name=query) | Q(email=query) |
                        Q(mobile_number=query) | Q(city=query)).order_by('id')
                    page = request.GET.get('page', 1)
                    paginator = Paginator(watchamanrecord, 10)
                    try:
                        watchmanrecord = paginator.page(page)
                    except PageNotAnInteger:
                        watchmanrecord = paginator.page(1)
                    except EmptyPage:
                        watchmanrecord = paginator.page(paginator.num_pages)

                return render(request, 'society/watchman_record.html', {'watchmanrecord': watchmanrecord})
            else:
                messages.success(request, 'You dont have any watchman')
                return render(request, 'society/watchman_record.html')
    else:
        messages.success(request, 'You dont have any watchman')
        return render(request, 'society/watchman_record.html')


def user_record(request):
    email = request.session.get('email')
    ss_record = Society_Secretry.objects.get(email=email)
    park_slot_records = Park_slot.objects.filter(society_id=ss_record.society_id)
    if park_slot_records:
        data = []
        for brecord in park_slot_records:
            id = brecord.id
            data.append(id)
        for zdata in data:
            zonerecord = Zone_Booking.objects.filter(park_slot_id=zdata)
            if zonerecord:
                data1 = []
                for zrecord in zonerecord:
                    userid = zrecord.vehicle.user.id
                    data.append(userid)
                for newdata in data:
                    newdata = User.objects.filter(id=newdata)
                    query = request.GET.get('newdata')
                    if query:
                        newdata = User.objects.filter(
                            Q(name=query) | Q(email=query) |
                            Q(mobile_number=query) | Q(city=query)).order_by('id')
                    page = request.GET.get('page', 1)
                    paginator = Paginator(newdata, 10)
                    try:
                        newdata = paginator.page(page)
                    except PageNotAnInteger:
                        newdata = paginator.page(1)
                    except EmptyPage:
                        newdata = paginator.page(paginator.num_pages)
                return render(request, 'society/user_record.html', {'data': newdata, 'newdata': newdata})

            else:
                messages.success(request, "sorry!!Your User Dont Have Any Booking For Zone")
                return render(request, 'society/user_record.html')
    else:
        messages.success(request, "sorry!!Your User Dont Have Any Booking For Zone")
        return render(request, 'society/user_record.html')


def zone_record(request):
    society_secretry = request.session.get('email')
    ss_record = Society_Secretry.objects.get(email=society_secretry)
    societyrecord = Society.objects.filter(id=ss_record.society_id)
    if societyrecord:
        data = []
        for brecord in societyrecord:
            id = brecord.id
            data.append(id)
        for zdata in data:
            zone_record = Park_slot.objects.filter(society_id=zdata)
            if zone_record:
                context = {
                    'zone_records': zone_record
                }
                return render(request, 'society/zone_records.html', context)
            else:
                messages.success(request, "You dont have any zone")
                return render(request, 'society/zone_records.html')
    else:
        messages.success(request, "You dont have any zone")
        return render(request, 'society/zone_records.html')


def Societysecretry_profile_view(request):
    email = request.session.get('email')
    print(email)
    if Society_Secretry.objects.filter(email=email).exists():
        societysecretry = Society_Secretry.objects.get(email=email)
        return render(request, 'society/parkzone_societysecretry_profile_view.html',
                      {'societysecretry': societysecretry})
    else:
        messages.success(request,"Profile view not found")
        return render(request, 'society/parkzone_societysecretry_profile_view.html')


def Societysecretry_profile_update(request):
    society_secretry = request.session.get('email')
    if request.method == "POST":
        id = request.POST['userid']
        data = Society_Secretry.objects.get(id=id)
        form = SocietySecretry_Form(request.POST, request.FILES, instance=data)
        validations = Society_Panel_Validations.soc_secretry_validations(form, Society_Secretry, "update")
        if validations == True:
            if form.is_valid():
                obj = form.save()
                loginupdate = Login.objects.get(number=obj.id)
                loginupdate.email = form['email'].value()
                loginupdate.password = form['password'].value()
                loginupdate.save()
                if society_secretry != loginupdate.email:
                    messages.success(request, 'Society Secretry Profile Edited Successfully')
                    return redirect("logout")
                else:
                    messages.success(request, 'Society Secretry Profile Edited Successfully')
                    return redirect('Societysecretry_profile_view')
            else:
                messages.error(request, validations)
        else:
            messages.error(request, validations)
            return render(request, 'society/parkzone_societysecretry_profile_edit.html', {'data': data, 'form': form})


def Societysecretry_Profile_edit(request):
    if request.method == "POST":
        print("hi")
        id = request.POST['userid']
        data = Society_Secretry.objects.get(id=id)
        form = SocietySecretry_Form(instance=data)
        return render(request, 'society/parkzone_societysecretry_profile_edit.html', {'data': data, 'form': form})
    else:
        return redirect('Societysecretry_profile_view')


@Parkzone_middleware
def park_slot_detail(request):
    email = request.session.get('email')
    data = Society_Secretry.objects.get(email=email)
    society = Society.objects.get(id=data.society_id)
    parking_slot = Park_slot.objects.filter(society_id=society.id)
    query = request.GET.get('parking_slot')
    if query:
        parking_slot = Park_slot.objects.filter(
            Q(slot_name=query)).order_by('-created_at')
    page = request.GET.get('page', 1)
    paginator = Paginator(parking_slot, 10)
    try:
        parking_slots = paginator.page(page)
    except PageNotAnInteger:
        parking_slots = paginator.page(1)
    except EmptyPage:
        parking_slots = paginator.page(paginator.num_pages)
    return render(request, 'society/Secretry_parking_slot_detail.html', {'parking_slot': parking_slots})


@Parkzone_middleware
def park_slot_detail_edit(request):
    id = request.POST['userid']
    if request.method == "POST":
        data = Park_slot.objects.get(id=id)
        form = Park_Slot_Form(instance=data)
        return render(request, 'society/Secretry_parking_slot_detail_edit.html', {'parking_slot': data, 'form': form})
    else:
        return redirect('park_slot_detail')


def park_slot_detail_update(request):
    if request.method == "POST":
        id = request.POST['id']
        data = Park_slot.objects.get(id=id)
        form = Park_Slot_Form(request.POST, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, 'Park Slot Details Edited Successfully')
            return redirect('park_slot_detail')
        else:
            messages.success(request, 'Park Slot Details Are Invalid')
            return redirect('park_slot_detail')
    else:
        return redirect('park_slot_detail')


@Parkzone_middleware
def park_slot_detail_create(request):
    if request.method == "POST":
        email = request.session.get('email')
        data = Society_Secretry.objects.get(email=email)
        society = Society.objects.get(id=data.society_id)
        society_parking_number = society.number_of_parking
        if Park_slot.objects.count() < society_parking_number:
            form = Park_Slot_Form(request.POST)
            validations = (form, Park_slot, "create")
            if validations:
                if form.is_valid():
                    form.save()
                    return redirect('park_slot_detail')
                else:
                    messages.error(request, validations)
                    return render(request, 'society/Secretry_parking_slot_detail_create.html', {'form': form})
        else:
            messages.success(request, 'Your Parking Slot is Full')
            return redirect('park_slot_detail')
    else:
        form = Park_Slot_Form()
        return render(request, 'society/Secretry_parking_slot_detail_create.html', {'form': form})


def pz_parking_owner_billing(request):
    if request.method == "POST":
        print(request.method)

        month = request.POST["month"]
        print("month", month)
        montharr = str(month).split("-")
        print(montharr)
        start_date = month + str("-01")
        if montharr[1] == '02':
            end_date = month + str("-29")
        if montharr[1] == '04' or montharr[1] == '06' or montharr[1] == '09' or montharr[1] == '09':
            end_date = month + str("-30")
        else:
            end_date = month + str("-31")

        x = Zone_Booking.objects.filter(booking_date__range=[start_date, end_date])
        data = []
        for y in x:
            parking_slot_id = y.park_slot_id
            data.append(parking_slot_id)
        for xdata in data:
            park_slot_owner = Park_Slot_Owner.objects.filter(park_slot_id=xdata)

            total = 0
            if park_slot_owner:
                wb = Workbook()
                sheet1 = wb.add_sheet('Sheet 1')
                sheet1.write(0, 0, "Name Of Account Holder")
                sheet1.write(0, 1, "Account Number")
                sheet1.write(0, 2, "Bank Name")
                sheet1.write(0, 3, "IFSC Code")
                sheet1.write(0, 4, "Branch")
                sheet1.write(0, 5, "Amount")
                i = 1

                for z in x:
                    total = total + z.booking_amount
                    print(total)

                for park_slot_owner in dict.values():
                    j = 0
                    acc_holder_name = park_slot_owner.name
                    account_Num = park_slot_owner.account_number
                    bank_Name = park_slot_owner.bank_name
                    ifsc_code = park_slot_owner.ifsc_code
                    branch = park_slot_owner.branch
                    sheet1.write(i, j, acc_holder_name)
                    j = j + 1
                    sheet1.write(i, j, account_Num)
                    j = j + 1
                    sheet1.write(i, j, bank_Name)
                    j = j + 1
                    sheet1.write(i, j, ifsc_code)
                    j = j + 1
                    sheet1.write(i, j, branch)
                    j = j + 1
                    sheet1.write(i, j, )
                    i = i + 1
                sheet1.write(i, j, total)

                xlspath = 'media/Reports/commision.xls'
                wb.save(xlspath)

                context = {
                    'summary_data': dict.values(),
                    'total': total,
                    'month': start_date,
                }
                print(dict.values())
                return render(request, 'ParkSlotOwner/parkzone_parkingowner_billing_report#.html', context)
            else:

                return render(request, 'ParkSlotOwner/parkzone_parkingowner_billing_report#.html',
                              {'message': 'Billing already done for this month'})


    else:
        if Park_Slot_Owner.objects.count() > 0:
            data = Park_Slot_Owner.objects.all()
            return render(request, 'ParkSlotOwner/parkzone_parkingowner_billing_report#.html', {
                'form': data,
            })
        else:
            return render(request, 'ParkSlotOwner/parkzone_parkingowner_billing_report#.html')

def society_view1(request):
    id = request.POST['id']
    society = Society.objects.filter(id=id)
    array = []
    for x in society:
        data = '<div class="row"> <div class="col-md-4"><h4><label>Name:</label></h4></div><div class="col-md-8">' + str(x.name) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Location:</label></h4></div><div class="col-md-8">' + str(
            x.location) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>City:</label></h4></div><div class="col-md-8">' + str(
            x.city) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>State:</label></h4></div><div class="col-md-8">' + str(
            x.state) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Country:</label></h4></div><div class="col-md-8">' + str(
            x.country) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>TwoWheel Hourly Price:</label></h4></div><div class="col-md-8">' + str(
            x.two_wheel_hourly_price) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>TwoWheel Weekly Price:</label></h4></div><div class="col-md-8">' + str(
            x.two_wheel_weekly_price) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Twowheel Monthly Price:</label></h4></div><div class="col-md-8">' + str(
            x.two_wheel_monthly_price) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>TwoWheel Daily Price:</label></h4></div><div class="col-md-8">' + str(
            x.two_wheel_daily_price) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>FourWheel Hourly Price:</label></h4></div><div class="col-md-8">' + str(
            x.four_wheel_hourly_price) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>FourWheel Weekly Price:</label></h4></div><div class="col-md-8">' + str(
            x.four_wheel_weekly_price) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Four Wheel Monthly Price:</label></h4></div><div class="col-md-8">' + str(
            x.four_wheel_monthly_price) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>FourWheel Daily Price:</label></h4></div><div class="col-md-8">' + str(
            x.four_wheel_daily_price) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Number of Parking:</label></h4></div><div class="col-md-8">' + str(
            x.number_of_parking) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Opening Time:</label></h4></div><div class="col-md-8">' + str(
            x.opening_time) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Closing Time:</label></h4></div><div class="col-md-8">' + str(
            x.closing_time) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Longtitude:</label></h4></div><div class="col-md-8">' + str(
            x.longtitude) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>langtitude:</label></h4></div><div class="col-md-8">' + str(
            x.langtitude) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>bank name:</label></h4></div><div class="col-md-8">' + str(
            x.bank_name) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>branch:</label></h4></div><div class="col-md-8">' + str(
            x.branch) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>account number:</label></h4></div><div class="col-md-8">' + str(
            x.account_number) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>ifsc code:</label></h4></div><div class="col-md-8">' + str(
            x.ifsc_code) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>commision:</label></h4></div><div class="col-md-8">' + str(
            x.commision) + '</div></div>'
        array.append(data)
    return HttpResponse(array)

def societyowner_view1(request):
    id = request.POST['id']
    print("hgiiii",id)
    societyowner = Society_Secretry.objects.filter(id=id)
    array = []
    for x in societyowner:
        data = '<div class="row"> <div class="col-md-4"><h4><label>Society:</label></h4></div><div class="col-md-8">' + str(x.society) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Name:</label></h4></div><div class="col-md-8">' + str(
            x.name) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Address:</label></h4></div><div class="col-md-8">' + str(
            x.address) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>State:</label></h4></div><div class="col-md-8">' + str(
            x.state) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>City:</label></h4></div><div class="col-md-8">' + str(
            x.city) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Country:</label></h4></div><div class="col-md-8">' + str(
            x.country) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>State:</label></h4></div><div class="col-md-8">' + str(
            x.state) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Mobile Number:</label></h4></div><div class="col-md-8">' + str(
            x.mobile_number) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Email:</label></h4></div><div class="col-md-8">' + str(
            x.email) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Password:</label></h4></div><div class="col-md-8">' + str(
            x.password) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Aadhar Card:</label></h4></div><div class="col-md-8">' + str(
            x.aadhar_card) + '</div></div>''<div class="row"><div class="col-md-4"><h4><label>Aadhar Number:</label></h4></div><div class="col-md-8">' + str(
            x.aadhar_num) + '</div></div>'
        array.append(data)
    return HttpResponse(array)


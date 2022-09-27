import re
def name_blank(request):
    name=request.data['name']
    if name=="":
        return False
    else:
        return True

def city_blank(request):
    city=request.data['city']
    if city=="":
        return False
    else:
        return True

def country_blank(request):
    city=request.data['country']
    if city=="":
        return False
    else:
        return True

def state_blank(request):
    city=request.data['state']
    if city=="":
        return False
    else:
        return True

def mob_num_exist(request,modelname):
    mobilenum=request.data['mobile_number']
    if modelname.objects.filter(mobile_number=mobilenum).exists():
        return False
    else:
        return True

def mobnum_Validation_API(request):
    data = request.data['mobile_number']
    x = re.search("^((\+){1}91){1}[1-9]{1}[0-9]{9}$", str(data))
    if not x:
        return False

def mob_num_blank(request):
    mobilenum=request.data['mobile_number']
    if mobilenum=="":
        return False
    else:
        return True

def email_exist(request,modelname):
    email=request.data['email']
    if modelname.objects.filter(email=email).exists():
        return False
    else:
        return True

def email_blank(request):
    email=request.data['email']
    if email=="":
        return False
    else:
        return True

def email_Validation_API(request):
    data = request.data['email']
    x = re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9-]{1,50}[.][a-zA-Z0-9-]{1,50}$", str(data))
    if not x:
        return False
    else:
        return True

def password_exist(request,modelname):
    password=request.data['password']
    if modelname.objects.filter(password=password).exists():
        return False
    else:
        return True

def password_blank(request):
    password=request.data['password']
    if password=="":
        return False
    else:
        return True

# def password_Validation_API(request):
#     data = request.data['password']
#     x = re.search("(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,20}$", str(data))
#     if not x:
#         return False
#     else:
#         return True

def confpassword_blank(request):
    confirm_password=request.data['confirm_password']
    if confirm_password=="":
        return False
    else:
        return True

def confpassword_Validation_API(request):
    data = request.data['confirm_password']
    data_pass = request.data['password']
    if data!=data_pass:
        return False
    else:
        return True

def user_exist(request,modelname):
    userid = request.POST['user']
    if modelname.objects.filter(id=userid).exists():
        return False
    else:
        return True

def vehicle_reg_no_exist(request,modelname):
    vehicle_reg_no=request.data['vehicle_registration_no']
    if modelname.objects.filter(vehicle_registration_no=vehicle_reg_no).exists():
        return False
    else:
        return True

def vehicleNum_Validation(request):
    data = request.data['vehicle_registration_no']
    x = re.search("^[A-Z]{2}[0-9]{1,2}(?: [A-Z])?(?: [A-Z]*)? [0-9]{4}$", str(data))                   ##############"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$
    if not x:
        return False
    else:
        return True

def driving_lic_no_exist(request,modelname):
    driving_lic_no=request.data['driving_lic_number']
    if modelname.objects.filter(driving_lic_number=driving_lic_no).exists():
        return False
    else:
        return True

def drivingLicNum_Validation(request):
    data = request.data['driving_lic_number']
    if str(data) != "":
        x = re.search("^(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}$", str(data))
        if not x:
            return False
        else:
            return True

def rc_book_no_exist(request,modelname):
    rc_book_no=request.data['rc_book_no']
    if modelname.objects.filter(rc_book_no=rc_book_no).exists():
        return False
    else:
        return True

def RCBookNum_Validation(request):
    data = request.data['rc_book_no']
    print(data)
    if str(data) != "":
        x = re.search("^[0-9]*$", str(data))
        if not x:
            return False
        else:
            return True



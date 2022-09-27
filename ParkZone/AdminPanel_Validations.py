import re


def mobnum_Validation(form, model):
    data = form['mobile_number'].value()
    x = re.search("^((\+){1}91){1}[1-9]{1}[0-9]{9}$", str(data))
    if not x:
        return False


def mobnum_exist_Validation(form, model):
    data = form['mobile_number'].value()
    if model.objects.filter(mobile_number=data).exists():
        return False


def email_Validation(form, model):
    data = form['email'].value()
    x = re.search("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$", str(data))
    if not x:
        return False


def email_exist_Validation(form, model):
    data = form['email'].value()
    data = str(data)
    if model.objects.filter(email=data).exists():
        return False


def vehicleNum_Validation(form, model):
    data = form['vehicle_registration_no'].value()
    x = re.search("^[A-Z]{2}[ -][0-9]{1,2}(?: [A-Z])?(?: [A-Z]*)? [0-9]{4}$", str(data))                   ##############"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$
    if not x:
        return False

def drivingLicNum_Validation(form, model):
    data = form['driving_lic_number'].value()
    if str(data) != "":
        x = re.search("^(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}$", str(data))
        if not x:
            return False


def RCBookNum_Validation(form, model):
    data = form['rc_book_no'].value()
    print(data)
    if str(data) != "":
        x = re.search("^[0-9]*$", str(data))
        if not x:
            return False

def vehicleNum_exist_Validation(form, model):
    data = form['vehicle_registration_no'].value()
    if model.objects.filter(vehicle_registration_no=data).exists():
        return False

def drivingLicNum_exist__Validation(form, model):
    data = form['driving_lic_number'].value()
    if model.objects.filter(driving_lic_number=data).exists():
        return False

def RCBookNum_exist__Validation(form, model):
    data = form['rc_book_no'].value()
    if model.objects.filter(rc_book_no=data).exists():
        return False

# def password_Validation(form, model):
#     data = form['password'].value()
#     x = re.search("(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z])$", str(data))
#     if not x:
#         return False


def password_exist_Validation(form, model):
    data = form['password'].value()
    if model.objects.filter(password=data).exists():
        return False


def age_Validation(form, model):
    data = form['age'].value()
    if str(data) != "" or not str(data).__contains__("Please enter age "):
        if not len(data) <= 2 :
            return False


def name_Validation(form, model):
    data = form['name'].value()
    print(data)
    if str(data) != "":
        x = re.search("^[a-zA-Z]+$", str(data))
        if not x:
            return False


def aadhar_Validation(form, model):
    data = form['aadhar_num'].value()
    print(data)
    if str(data) != "":
        x = re.search("^\d{4}\d{4}\d{4}$", str(data))
        if not x:
            # "Please enter valid aadhar number"
            return False

def soc_exist(form, model):
    data = form['name'].value()
    if model.objects.filter(name=data).exists():
        return False

def zone_exist(form, model):
    data = form['slot_name'].value()
    if model.objects.filter(slot_name=data).exists():
        return False



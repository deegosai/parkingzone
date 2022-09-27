from ParkZone.AdminPanel_Validations import *


def validations( form,model,status):
    if status=="create":
        if mobnum_Validation(form, model) == False:
            msg = "Mobile Number must be entered in the format: '+91<mobilenumber> with 10 digits"
            return msg
        elif mobnum_exist_Validation(form, model) == False:
            msg = "Mobile Number already exists. please insert another."
            return msg
        elif email_Validation(form, model) == False:
            msg = "Email is invalid. please insert proper email."
            return msg
        elif email_exist_Validation(form, model) == False:
            msg = "Email already exists. please insert proper email."
            return msg
        # elif password_Validation(form, model) == False:
        #     msg = "Please enter Correct Password (at least one upper case, one lower case, one digit, " \
        #           "one special character of length 8)"
        #     return msg
        elif password_exist_Validation(form, model) == False:
            msg = "Password exists please try another"
            return msg
        elif age_Validation(form,model)==False:
            msg= "Please enter proper age"
            return msg
        else:
            return True

    elif status=="update":
        if mobnum_Validation(form, model) == False:
            msg = "Mobile Number must be entered in the format: '+91<mobilenumber> with 10 digits"
            return msg
        elif email_Validation(form, model) == False:
            msg = "Email is invalid. please insert another."
            return msg
        # elif password_Validation(form, model) == False:
        #     msg = "Please enter Correct Password (at least one upper case, one lower case, one digit, " \
        #           "one special character of length 8)"
        #     return msg
        elif age_Validation(form,model)==False:
            msg= "Please enter proper age"
            return msg
        else:
            return True


def vehicle_Validation( form,model):
    if RCBookNum_exist__Validation(form,model) == False:
        msg = "RC Book Number already exists"
        return msg
    elif drivingLicNum_exist__Validation(form, model) == False:
        msg = "Driving Licence Number already exists"
        return msg
    elif vehicleNum_exist_Validation(form, model) == False:
        msg = "Vehicle Number already exists"
        return msg
    elif RCBookNum_Validation(form, model) == False:
        msg = "Please enter valid 12 digit RC book number"
        return msg
    elif drivingLicNum_Validation(form, model) == False:
        msg = "Please enter valid Driving Licence Number"
        return msg
    # elif vehicleNum_Validation(form, model) == False:
    #     msg = "Please enter valid Vehicle Registration Number"
    #     return msg

    else:
        return True
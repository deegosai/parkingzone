from ParkZone.API_Validation import *


def userAPI_Validations(request, User,status):
    if status=="create":
        if name_blank(request) == False:
            return "1 : Name is blank"
        elif email_exist(request, User) == False:
            return "2 : Email already exists. Try another one"
        elif email_blank(request) == False:
            return "3 : Email is blank"
        elif email_Validation_API(request) == False:
            return "4 : Email is invalid. please insert proper email."
        elif mob_num_exist(request, User) == False:
            return "5 : Mobile number already exists. Try another one"
        elif mob_num_blank(request) == False:
            return "6 : Mobile number is blank"
        elif mobnum_Validation_API(request) == False:
            return "7 : Mobile Number must be in the format'+91<mobilenumber> with 10 digits"
        elif password_exist(request, User) == False:
            return "8 : Password already exists. Try another one"
        elif password_blank(request) == False:
            return "9 : Password is blank"
        # elif password_Validation_API(request) == False:
        #     return "10 : Please enter Correct Password (at least one upper case, one lower case, one digit)"
        elif confpassword_blank(request) == False:
            return "11 : Confirm Password is blank"
        elif confpassword_Validation_API(request) == False:
            return "12 : Confirm Password didn't Match"
        else:
            return True
    elif status=="update":
        if name_blank(request) == False:
            return "1 : Name is blank"
        elif email_blank(request) == False:
            return "2 : Email is blank"
        elif email_Validation_API(request) == False:
            return "3 : Email is invalid. please insert proper email."

        else:
            return True


def userVehicle_API_Validations(request, UserVehicle,status):
    if status=="create":
        if vehicle_reg_no_exist(request, UserVehicle) == False:
            return "2 : Vehicle register number already exists. Try another one"
        else:
            return True
    elif status=="update":
        if vehicleNum_Validation(request) == False:
            return "2 : Enter valid vehicle register number"
        elif drivingLicNum_Validation(request) == False:
             return "3 : Enter valid driving licence number"
        elif RCBookNum_Validation(request) == False:
             return "4 : Enter valid RC book number "
        else:
            return True


def user_login_API_Validations(request, User):
    if password_blank(request) == False:
        return "2 : Password is blank"
    # elif password_Validation_API(request) == False:
    #     return "3 : Please enter Correct Password"
    else:
        return True

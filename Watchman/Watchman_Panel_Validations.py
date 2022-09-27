from ParkZone.AdminPanel_Validations import *


def watchman_validations(form, model, status):
    if status == "create":
        if mobnum_Validation(form, model) == False:
            msg = "Mobile Number must be entered in the format: '+91<mobilenumber> with 10 digits"
            return msg
        elif mobnum_exist_Validation(form, model) == False:
            msg = "Mobile Number already exists. please insert another."
            return msg
        elif email_Validation(form, model) == False:
            msg = "Email is invalid. please insert another."
            return msg
        elif email_exist_Validation(form, model) == False:
            msg = "Email already exists. please insert another."
            return msg
        elif password_exist_Validation(form, model) == False:
            msg = "Password exists please try another"
            return msg
        elif aadhar_Validation(form,
                               model) == False:
            msg = "Please enter valid aadhar number"
            return msg
        else:
            return True

    elif status == "update":
        if mobnum_Validation(form, model) == False:
            msg = "Mobile Number must be entered in the format: '+91<mobilenumber> with 10 digits"
            return msg
        elif email_Validation(form, model) == False:
            msg = "Email is invalid. please insert another."
            return msg
        elif aadhar_Validation(form,
                               model) == False:
            msg = "Please enter valid aadhar number"
            return msg
        else:
            return True

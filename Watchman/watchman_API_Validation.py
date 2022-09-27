from ParkZone.API_Validation import *


def watchmanAPI_Validations(request, User):
    if mob_num_exist(request, User) == False:
        return "2 : Mobile number already exists. Try another one"
    elif email_exist(request, User) == False:
        return "3 : Email already exists. Try another one"
    elif password_exist(request, User) == False:
        return "4 : Password already exists. Try another one"
    else:
        return True


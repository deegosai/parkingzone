from ParkZone.AdminPanel_Validations import *



def zone_validations( form,model,status):

    if zone_exist(form, model) == False:
        msg = "Slot Name Is already exists"
        return msg





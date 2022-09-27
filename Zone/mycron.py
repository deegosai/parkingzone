import urllib

import schedule
from django.db.models import Q
import datetime
import random
from Zone.models import Zone_Booking
import time

class cronSMS():
    bookings = Zone_Booking.objects.filter(Q(activated_package="Monthly") | Q(activated_package="Weekly"))
    arr = []
    for x in bookings:
        print(x)
        expiry_date = x.activated_package_expire
        todayDate = datetime.datetime.today().date()
        print(todayDate)
        otp = random.randint(100000, 999999)
        print("todayDate < expiry_date===========",todayDate < expiry_date)
        print("todayDate == expiry_date===========", todayDate == expiry_date)
        if todayDate < expiry_date or todayDate==expiry_date:
            print("in expire====>>>", todayDate < expiry_date)
            booking_mobile_number = x.vehicle.user.mobile_number
            # dict[x]=booking_mobile_number
            if len(booking_mobile_number)>10:
                mob_no=str(booking_mobile_number).replace("+91","")
                arr.append(int(mob_no))
            else:
                arr.append(booking_mobile_number)
    print("********************************                               ***********************************")
    print("                                    Hi !!!! Megha ....                                             ")
    print("******************************** "+str(len(arr))+"                              *************************************")
    for y in arr:
        print("booking mobile num----->>>", y)
        otp = random.randint(100000, 999999)
        print("otp----->>>", otp)
        print("hey-http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number=y&message=' + str(otp)")
        request_url = urllib.request.urlopen(
            'http://panel.adcomsolution.in/http-api.php?username=varun&password=varun123&senderid=LUCSON&route=1&number='+str(y)+'&message=' + str(otp))


schedule.every(120).seconds.do(cronSMS)####day.at("00:05").do(MyCronJob)  ####.every(10).seconds.do(cronSMS)
while 1:
    schedule.run_pending()
    time.sleep(1)
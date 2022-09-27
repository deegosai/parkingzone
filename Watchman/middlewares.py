from django.shortcuts import render, redirect
def Parkzone_middleware(get_response):
    def my_function(request):
        if not request.session.get('email'):
            return redirect("adminlogin")
        else:
            response = get_response(request)
            return response
    return my_function
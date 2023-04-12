from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('mainpage')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func    

def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            check = False
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()#[0].name

                for i in group:
                    if str(i) in allowed_roles:
                        check = True
            if check:
                return view_func(request, *args, **kwargs)            
            else:
                return HttpResponse(f'You have to be {allowed_roles} to see this page!')     
        return wrapper_func
    return decorator        
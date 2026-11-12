from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import get_user_model
#from .models import CustomUser

def email_verified_required(view_func):
    user= get_user_model()
    def _wrapped_view(request,*args, **kwargs):
        if request.user.is_authenticated and request.user.email_verified:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('email_confirmation')

    return _wrapped_view
def user_authentication_required(view_func):
    user = get_user_model
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/')
    return _wrapped_view

from django.shortcuts import render, redirect
from functools import wraps
from django.conf import settings
from django.contrib.auth.decorators import user_passes_test

def unauthenticated(function):
    """Limit view to authenticated users only."""
    def _inner(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')          
        return function(request, *args, **kwargs)
    return _inner

def authenticated(function):
    """Limit view to unauthenticated users only."""
    def _inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('main')          
        return function(request, *args, **kwargs)
    return _inner

def isstaff(function):
    def _inner(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff == False:
                return redirect('main')
            return function(request, *args, **kwargs)
        return redirect('main')
    return _inner
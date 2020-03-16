from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm

# Create your views here.
def index(request):
    return render (request, 'index.html')

@login_required 
def logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('index'))
    
def login(request):
    """Returns the login page"""
    login_form = UserLoginForm()
    return render(request, 'login.html', {
        'form':login_form         
    })

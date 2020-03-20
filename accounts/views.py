from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from .forms import UserLoginForm, UserRegistrationForm

# Create your views here.
def index(request):
    return render (request, 'index.html')

@login_required 
def logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully been logged out")
    return redirect(reverse('index'))
    
def login(request):
    """Return a login page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == 'POST':
        
        login_form = UserLoginForm(request.POST) # populate the form from what the user has keyed in
        if login_form.is_valid():
            # attempt to check the username and password is valid
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password'])
            messages.success(request, "You have successfully logged in")
            if user:
                # log in the user
                auth.login(user=user, request=request)
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Invalid username or password")
                return render(request, 'login.html', {
                  'form':login_form,
                  'error_message': 'Invalid username or password',
                })

    else:
        error_message = ''
        login_form = UserLoginForm()
        return render(request, 'login.html', {
            'form':login_form,
            'error_message': ''
        })

def registration(request):
    """Render the registration page"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
            # NEW CODE STARTS HERE
        if form.is_valid():
            #1 create the user
            form.save()

            #2 check if the user has been created properly
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                #3 if the user has been created successful, attempt to login
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered")
            else:
                messages.error(request, "Unable to register your account at this time")
            return redirect(reverse('index'))
        #NEW CODE ENDS HERE
        else:
            return render(request, 'registration.html', {
                'form':form
            })
            
    else :
        registration_form = UserRegistrationForm()
        return render(request, 'registration.html', {
            "form": registration_form})    
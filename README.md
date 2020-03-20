
# SETTING UP DJANGO ON AWS USING PYTHON
---
#### INSTALLING DJANGO

1. In the terminal, type

        pip3 install django==2.2.4
        
        - may change when django is updated 

2. Start a new project named <PROJECT_NAME> in the current directory.\
    Note the "**DOT**" at the end of the command.

        django-admin startproject <PROJECT NAME> .

3. Set the ALLOWED_HOST in the <project name>/settings.py 

        ALLOWED_HOST = ['<DOMAIN_NAME'> or '*' ]
        - putting '*' will allow it to run from anywhere 
        
4. Run the server and see if it works

        python3 manage.py runserver localhost:8080

5. Create .gitignore file

        touch .gitignore
        
    refer to the .gitignore file content for items to be added
    
---
#### CREATE THE ACCOUNTS APP

1. In the bash terminal, type in the command.\
    Stop the server by pressing CTRL+C (if the server is running)\
    Create a new app in the terminal -- you should see a new folder being created.

        django-admin startapp accounts

2. CREATE A CUSTOM USER MODEL\
    Inside accounts/models.py, add in the following

        from django.contrib.auth.models import AbstractUser
        from django.db import models
    
        # Create your models here.
        class MyUser(AbstractUser):
        pass

    Note: if you want to have fields in your custom MyUser, just add to it normally as if it is any other model.

3. Use the custom MyUser as default authentication model\
    Inside <project folder>/settings.py, add the following to as last lines:

        AUTH_USER_MODEL = 'accounts.MyUser' 
        
        AUTHENTICATION_BACKENDS = (
            # Needed to login by custom User model, regardless of `allauth`
            "django.contrib.auth.backends.ModelBackend",
            'accounts.backends.CaseInsensitiveAuth' 
        )
        
4.  INSTALL THE APP\
    Also inside settings.py, include the newly created app (highlighted in yellow)

        INSTALLED_APPS = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
        --> 'AppName'
        ]

5. Register the custom user, so can view in the admin portal.\
    Inside accounts/admin.py, register the custom user model.

        from django.contrib import admin
        from .models import MyUser
        
        # Register your models here.
        admin.site.register(MyUser)

---
###  SETTING UP THE PROJECT DEPENDENCIES

#### SETUP FOR TEMPLATES INHERITANCE

Create a new folder name 'templates' in the same level as the project folder and then modify settings.py:

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
        --->    'DIRS': [os.path.join(BASE_DIR, 'templates')],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                        
                    ],
                },
            },
        ]

#### SETUP STATIC FOLDER
To use static files (JavaScript, CSS etc), we must first instruct Django where to locate the static files. 
- Step 1: Inside <project folder>/settings.py, add this at the bottom of the file:
    ###### enable static files

        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, "static")
        ]

- Step 2: Create a folder named static, on the same level as the project folder

- Step 3: Use the static function to load static files. You have to import the static function into your template. See below for an example:

        {% load static %} <----
        <!doctype html>
        <html lang="en">
          <head>
            <!-- Required meta tags -->
            <link rel="stylesheet" href="{% static 'styles.css' %}" type="text/css" />
            <title>Hello, world!</title>
          </head>

#### MOVING URLs INTO ITS OWN APP

Right now the URLs for the accounts app is inside <project folder>/settings.py.
This is not ideal; it makes our app harder to swap out.

The first thing we will do is to move all the accounts paths from <project folder>/settings.py to its own urls.py inside the accounts app.

Create  a new file as accounts/urls.py and enter the following:
        
        from django.urls import path, include.
        from .views import index, logout, login, profile, register
        
        urlpatterns = [
            path('', index, name='index'),
        ]


Make sure you remove those urls from the <project folder>/urls settings.py. We also have to include the account/urls.py

This should be our <project folder>/urls.py

        from django.contrib import admin
        from django.urls import path
        from django.urls import include
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('accounts.urls')),
        ]

To test it, run your app, and try to access it at account/inde x

#### SET UP BOOTSTRAP FORM

    sudo pip3 install django-forms-bootstrap

Also inside settings.py, include the 'django\_forms\_bootstrap'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    --> 'django_forms_bootstrap',
        'AppName'
    ]
    
#### SETUP MESSAGE STORAGE

Add this at the bottom of settings.py:\
Purely to fix an issue with Cloud9

        MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

---
#### CREATE MIGRATION AND RUN
1. In the bash terminal, type:

        python3 manage.py makemigrations
        python3 manage.py migrate

#### CREATE SUPERUSER

1. In the bash terminal, type:

        python3 manage.py createsuperuser

2. Run the server and add in "/admin" to assess the admin portal    
         
---

---
## USER AUTHENTICATION SETUP INSTRUCTIONS

###  ADD A LOGOUT ROUTE
##### _Views.py_
Insides accounts/views.py, we are going to import **django.contrib.auth** which holds a lot of login and logout functions.

        from django.shortcuts import render, redirect, reverse, HttpResponse
        from django.contrib import auth, messages

        # Create your views here.
        def index(request):
            return render(request, 'index.html')
            
        def logout(request):
            auth.logout(request)
            messages.success(request, "You have successfully been logged out")
            return redirect(reverse('index'))

##### _/templates/index.html_
Now we update the index.html template to show the messages, and to show the logout link.
        
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Document</title>
        </head>
        <body>
            <h1>Hello!</h1>
        ->  {% if request.user.username %}
            Logged In As : {{request.user.username}}
            {% endif %}
            
            <hr> 
            {% if messages %}
            <div>
                {% for message in messages %} {{ message }} {% endfor %}
            </div>
        ->  {% endif %}
            
            <ul>
                <li>Login</li>
                <li>Register</li>
                <li>Profile</li>
        --->    <li><a href="{% url 'logout' %}">Logout</a></li>
            </ul>
        </body>
        </html>

##### _accounts.urls.py_

        from accounts.views import index, logout
        
        urlpatterns = [
            path('', index, name='index'),
            path('logout/', logout, name='logout')
        ]

---
### CREATE LOGIN PAGE AND FORM FOR ENTRY

#### SETUP THE LOGIN PAGE
Setup the view, template and url for the login page;

##### _accounts/view.py_

        def login(request):
            """Returns the login page"""
            return render(request, 'login.html')
        
##### _accounts/templates/login.html_

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Document</title>
        </head>
        <body>
            <h1>User Login</h1>
           
        </body>
        </html>

##### _accounts folder/urls.py_

        from accounts.views import index, logout, login

        urlpatterns = [
            path('', index, name='index'),
            path('logout/', logout, name='logout'),
            path('login/', login, name='login')
        ]

##### _accounts/template/index.html_
Update accounts/template/index.html to enable the link to the login page:

        <body>
        …   
            <ul>
        --->    <li><a href="{% url 'login' %}">Login</a></li>
                <li>Register</li>
                <li>Profile</li>
                <li><a href="{% url 'logout' %}">Logout</a></li>
                
            </ul>
        </body>
        </html>

#### CREATE THE LOGIN FORM
Create a forms.py inside the accounts folder, and put down its content:

        from django import forms
        
        class UserLoginForm(forms.Form):
            """Form to login user"""
            username = forms.CharField()
            password = forms.CharField(widget=forms.PasswordInput)

#### PUT THE FORM INTO THE PAGE
Inside accounts/views.py, import the form which we have just created and assign it to a placeholder in the template:
        
        from accounts.forms import UserLoginForm
        
        def login(request):
            """Returns the login page"""
            login_form = UserLoginForm()
            return render(request, 'login.html', {
                'form':login_form         
            })

After which, inside login.html, render the form. Remember the CSRF token!

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Document</title>
        </head>
        <body>
            <h1>User Login</h1>
           
        --> <form method='POST'>
                 {% csrf_token %}
                 {{ form.as_p }}
                 <input type="submit">
        --> </form>
        </body>
        </html>

#### Handle the Login
Add in the following code to the login function at accounts/views.py

    def login(request):
        """Returns the login page"""
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
                      'form':login_form
                    })
        else:
            login_form = UserLoginForm()
            return render(request, 'login.html', {
                'form':login_form
            })

Also add display of session messages inside login.html

    <body>
        <h1>User Login</h1>
       
        <form method='POST'>
             {% csrf_token %}
             {{ form.as_p }}
             <input type="submit">
        </form>
        
          <hr> {% if messages %}
        <div>
            {% for message in messages %} {{ message }} {% endfor %}
        </div>
        {% endif %}
    </body>

### SETTING UP FOR USER LOGIN

Add to settings.py the default login URL
    
    LOGIN_URL = 'login'

#### @login\_required and user.is\_authenticated

###### PREVENT LOGIN PAGE WHEN USER IS LOGGED IN
Go to accounts.view.py, add in the following line in the **login** function

    def login(request):
        """Return a login page"""
        if request.user.is_authenticated:     <----
            return redirect(reverse('index')) <----
            ....
  
###### REDIRECT BACK TO INDEX WHEN USER IS LOGGED OUT
Add @login_required infront of the logout function

    @login_required  <---
    def logout(request):
        auth.logout(request)
        messages.success(request, "You have successfully been logged out")
        return redirect(reverse('index'))

### SETUP REGISTRATION FORM
We are now going to create a page to show a registration form. As usual, we need a function inside views.py, a tpath in urls.py and then a template.

#### CREATE REGISTRATION FUNCTION
###### Inside account/views.py:

    def register(request):
       return render(request, 'register.html')

###### Inside <project folder>/urls.py
    
    from django.contrib import admin
    from django.urls import path
    from accounts.views import index, logout, login, profile, register

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', index, name='index'),
        path('logout/', logout, name='logout'),
        path('login/', login, name='login'),
        path('profile/', profile),
        path('register/', register, name='register')]

###### account/templates/register.html

    {% extends 'base.html' %}
    {% block page_title %}Registration Page{% endblock %}
    {% block page_heading %}User Registration{% endblock %}
    {% block content %}
    <p>If you already have an account, you can <a href="{% url 'login' %}">sign in </a></p>
    {% endblock %}

#### ADD THE REGISTRATION FORM
###### account/forms.py
Add in the form below, make the following changes. The ones highlighted in green are for our custom user model to work.

    #Remember to import the below
    from django.contrib.auth.models import User
    from django.contrib.auth.forms import UserCreationForm
    from django.core.exceptions import ValidationError
    from .models import MyUser

    class UserRegistrationForm(UserCreationForm):
        """Form used to register a new user"""
    
        password1 = forms.CharField(widget=forms.PasswordInput)
        password2 = forms.CharField(
            label="Password Confirmation",
            widget=forms.PasswordInput)
        
        class Meta:
            model = User MyUser
        fields = ['email', 'username', 'password1', 'password2']

###### Create the form inside the view function register:
Remember to import in the **UserRegistrationForm** (see #1)

    from .forms import UserLoginForm, UserRegistrationForm  #1
    def register(request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {
            'form':form
        })

###### _accounts/templates/register.html_

    {% extends 'base.html' %}
    {% block page_title %}Registration Page{% endblock %}
    {% block page_heading %}User Registration{% endblock %}
    {% block content %}
    <p>If you already have an account, you can <a href="{% url 'login' %}">sign in </a></p>
    <form method='POST'>
        {% csrf_token %}
        {{ form.as_p }}
        <input type='submit'/>
    </form>
    {% endblock %}

#### Add in validation
We will add in rules to the form to make sure that the user enters valid information for the field. While we are able to check the length of the data and all that just with the various model fields, we have to write additional logic to check for length of password, if both passwords are key in properly and so on.

###### _accounts.forms.py_
Inside the class UserRegistrationForm (in forms.py), add this class after Meta (do not indent under Meta!)
Make sure you have this import at the top

    from django.contrib.auth import get_user_model
    
    #Add the following to the registration form
    def clean_email(self):
        User = get_user_model()
        email = self.cleaned_data.get('email') **#1**
        username = self.cleaned_data.get('username')
        **#2** check if the email is unique, using the Django ORM
        if User.objects.filter(email=email):
            raise forms.ValidationError(u'Email address must be unique')
        return email

At **#1**, we get a cleaned version of the email. By cleaned, we mean that all special characters inside the field has been processed so it won't cause issues when added into the database (like say, SQL injection).
For **#2**, we use Django ORM to check if the email is already in use. 

We will next add in the validation for the password:

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Please confirm your password")
        
        if password1 != password2:
            raise ValidationError("Passwords must match")
        
        return password2

#### Process the Form PART A -- validation 
The usual structure for a view function that process a form is:


###### _accounts/views.py_
Warning -- this is an example boilerplate for a function that process form. This is not working code!
    def your_generic_view_function_with_form(request):
        # if a form is submitted
        if request.method == 'POST':
            form = MyForm(request.POST)
            if form.is_valid():
                # do processing
                # after finished processing
                return redirect('path_to_redirect_to')
        else:
            # just show the form
            form = MyForm()
            return render(request, 'whatever_template_you_want.html',{
                'form': form
            })

So for our case, we will change the register() view function in accounts/views.py to:

    def register(request):
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
            if form.is_valid(): #1 check if the entry to the form are valid
                pass
            else:
                #2 if not valid, return the form to the view to show the errors
                return render(request, 'register.html', {
                    'form':form
                })
        else:
            form = UserRegistrationForm()
            return render(request, 'register.html', {
                'form':form
            })

At **#1**, we will use the is_valid() function to check if the data the user has submitted fits our validation rules (defined in step 3 above). Then for #2, if there are invalid entries, we will just re-render the form. The validation errors will show automatically.

#### 4B - Process the Form PART B -- add in the user if all fields are proper
If the form passed all the tests (i.e, form.is_valid() returns true), then we can proceed to add in the new user. Make the following adjustments to register()

    def register(request):
        User = get_user_model()
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
                return render(request, 'register.html', {
                    'form':form
                })
        else:
            form = UserRegistrationForm()
            return render(request, 'register.html', {
                'form':form
            })

With this, you will be able to register a user.

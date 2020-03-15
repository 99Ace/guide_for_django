
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
         
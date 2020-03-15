from django.urls import path
from accounts.views import index

urlpatterns = [
    path('', index, name='index')
    ]

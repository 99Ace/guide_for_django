from django.urls import path
from accounts.views import index, logout

urlpatterns = [
    path('', index, name='index'),
    path('logout/', logout, name='logout')
    ]

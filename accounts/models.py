from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class MyUser(AbstractUser):
    
    User_nickname = models.CharField(
        'Online Nickname',
        max_length = 10,
        blank = True,
        default = '')
        
    User_id = models.CharField(
        'NRIC last 4-char',
        max_length = 4,
        blank=True,
        default = '')
        
    Add_block_house = models.CharField(
        'Block / House No.',
        max_length = 6,
        blank=True,
        default = '')
    Add_street_name = models.CharField(
        'Street Name',
        max_length = 20,
        blank=True,
        default = '')
    Add_postal_code = models.CharField(
        'Postal Code',
        max_length = 6,
        blank=True,
        default = '')
    Contact_number = models.CharField(
        'Contact Number',
        max_length = 8,
        blank=True,
        default = ''
        )
    GENDER = [
        ('male','male'),
        ('female','female'),
        ('undisclosed','undisclosed')
        ]
    Gender = models.CharField(
        max_length = 10,
        blank=True,
        default = '')
        
    Date_of_birth = models.DateField ( 
        'Date of Birth',
        blank=True,
        default = timezone.now)
    
    
    pass
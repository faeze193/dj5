from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import Manager
from django_jalali.db import models as jmodels

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=99)
    last_name = models.CharField(max_length=99)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_admin =  models.BooleanField(default=False)

    subject = Manager()

    REQUIRED_FIELDS = ["email","first_name","last_name"]
    USERNAME_FIELD = 'phone'


    def __str__(self):
        return self.phone

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.Case, related_name='useradress')
    ostan = models.CharField(max_length=50)
    shahrestan = models.CharField(max_length=70)
    full_adress = models.TextField()
    codeposty = models.PositiveBigIntegerField()
    phone_number = models.PositiveBigIntegerField()
    email = models.EmailField(blank=True, null=True)
    

    

class Otp(models.Model):
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    created = jmodels.jDateTimeField(auto_now=True)
     


    
    



    

from random import random

from attr.validators import min_len
from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.db.models import SET_NULL

from accounts_app.models import BaseModel, User


# Create your models here.

class ClientProfile(BaseModel):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other","Other")
    )

    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default="male")
    profile_image = models.ImageField(upload_to="client_image/", null=True, blank=True)
    assigned_staff = models.ForeignKey(User,on_delete=SET_NULL,null=True,related_name="assigned_clients")
    date_of_birth = models.DateField(null=True,blank=True)
    occupation = models.CharField(max_length=50,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=20, null=True,blank=True)
    pincode = models.PositiveIntegerField(null=True,blank=True)
    state = models.CharField(null=True,blank=True)



    def __str__(self):
        return f"{self.email}"
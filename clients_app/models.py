from attr.validators import min_len
from django.db import models
from django.db.models import SET_NULL

from accounts_app.models import BaseModel, User, StaffProfile


# Create your models here.

class ClientProfile(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="client_profile")
    assigned_staff = models.ForeignKey(StaffProfile,on_delete=SET_NULL,null=True,related_name="assigned_clients")
    date_of_birth = models.DateField(null=True,blank=True)
    occupation = models.CharField(max_length=15,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    city = models.CharField(max_length=20, null=True,blank=True)
    pincode = models.PositiveIntegerField(null=True,blank=True)
    state = models.CharField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.email}"
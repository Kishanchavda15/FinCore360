from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from fincore_user_app.managers import UserManager


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractBaseUser, PermissionsMixin, BaseModel):

    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
    )

    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("client", "Client"),
    )

    full_name = models.CharField(max_length=255, blank=True, null=True)

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=15)

    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        default="male"
    )

    address = models.TextField(blank=True, null=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="client"
    )

    profile_image = models.ImageField(
        upload_to="user_image/",
        null=True,
        blank=True
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class OtpVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    otp = models.CharField(max_length=4)
    is_verify = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    create_at=models.DateTimeField(default=timezone.now)

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.email}-{self.otp}"
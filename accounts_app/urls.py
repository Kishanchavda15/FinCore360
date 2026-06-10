
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from accounts_app.views import RegisterUser, LoginUser, SendOtp, ForgotPassword, UpdateProfile

User_Urls = [
    path("user/register/", RegisterUser.as_view()),
    path("user/login/", LoginUser.as_view()),
    path("user/send-otp/", SendOtp.as_view()),
    path("user/forgot-password/", ForgotPassword.as_view()),
    path("user/profile/", UpdateProfile.as_view()),
]

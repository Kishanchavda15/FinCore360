
from django.urls import path,include
from rest_framework.routers import DefaultRouter

from accounts_app.views import RegisterUser, LoginUser
user_urlpatterns=[
    path("user/Register/Api/",RegisterUser.as_view()),
    path("user/LoginUser/Api/",LoginUser.as_view()),
]


from django.urls import path

from clients_app.views import ClientCreateApi, ClientUpdateApi

ClientProfile_Urls =[
    path("client/create/",ClientCreateApi.as_view()),
    path("client/update/",ClientUpdateApi.as_view())
]
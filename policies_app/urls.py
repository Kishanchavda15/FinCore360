from rest_framework.urls import path

from policies_app.views import PolicyCreateAPI, PolicyGet

Policy_Urls=[
    path("policy/create/",PolicyCreateAPI.as_view()),
    path("policy/get/",PolicyGet.as_view()),
]
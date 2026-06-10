from django.urls import path

from policies_app.views import (PolicyCreateAPI, PolicyRetrieveUpdateDeleteAPI)

Policy_Urls = [
    path("policy/create/", PolicyCreateAPI.as_view(), name="policy-create"),
    path("policy/<int:pk>/", PolicyRetrieveUpdateDeleteAPI.as_view(), name="policy-detail"),
]

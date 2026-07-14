"""
URL configuration for fincore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include

from accounts_app.urls import User_Urls
from clients_app.urls import ClientProfile_Urls
from documents_app.url import Documents_Urls
from notifications_app.urls import Notification_Urls
from policies_app.urls import Policy_Urls
from django.conf import settings
from django.conf.urls.static import static
from products_app.urls import Product_Urls

urlpatterns = [
    path("auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
    path("",include(User_Urls)),
    path("",include(ClientProfile_Urls)),
    path("",include(Policy_Urls)),
    path("",include(Documents_Urls)),
    path ("",include(Notification_Urls)),
    path ("",include(Product_Urls))
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
from django.contrib import admin

from clients_app.models import ClientProfile


# Register your models here.
@admin.register(ClientProfile)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "full_name", "email", "password", "phone_number", "gender", "profile_image", "assigned_staff",
                    "date_of_birth", "occupation", "address", "city", "pincode", "state"]

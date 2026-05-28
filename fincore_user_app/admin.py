from django.contrib import admin

from fincore_user_app.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display =["id","full_name","email","phone_number","gender","address","role"]
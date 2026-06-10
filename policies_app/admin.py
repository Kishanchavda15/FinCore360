from django.contrib import admin

from policies_app.models import Policy


# Register your models here.
@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "client",
        "staff",
        "product_type",
        "product_subtype",
        "amount",
        "status",
        "start_date",
    )
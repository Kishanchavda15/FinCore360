from django.contrib import admin
from notifications_app.models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "client",
        "policy",
        "title",
        "channel",
        "status",
        "reminder_date",
        "created_at_notification",  # FIXED HERE
    )
from django.db import models
from clients_app.models import ClientProfile
from policies_app.models import Policy


# Create your models here.

class Notification(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    message = models.TextField()

    reminder_date = models.DateTimeField()  # when to trigger

    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("sent", "Sent"), ("failed", "Failed")],
                              default="pending")
    channel = models.CharField(max_length=20, choices=[("email", "Email"), ("telegram", "Telegram"), ])
    created_at_notification = models.DateTimeField(auto_now_add=True)

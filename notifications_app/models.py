from django.db import models
from clients_app.models import ClientProfile
from policies_app.models import Policy


# Create your models here.

class Notification(models.Model):
    client = models.ForeignKey(ClientProfile, on_delete=models.CASCADE)
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    message = models.TextField()

    reminder_date = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20, db_index=True,
                              choices=[("pending", "Pending"), ("sent", "Sent"), ("failed", "Failed")],
                              default="pending")
    channel = models.CharField(max_length=20, choices=[("email", "Email"), ("telegram", "Telegram"), ])
    send_mode = models.CharField(
        max_length=20,
        choices=[("auto", "Auto"), ("manual", "Manual")],
        default="auto"
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)

    created_at_notification = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.client.email}"

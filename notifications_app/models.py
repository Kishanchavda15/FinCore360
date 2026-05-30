from django.db import models

from accounts_app.models import User


# Create your models here.

class Notification(models.Model):
    CHANNEL_CHOICES = (
        ("email", "EMAIL"),
        # ("telegram", "TELEGRAM"),
        # ("whatsApp", "WHATSAPP")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")

    title = models.CharField(max_length=255)
    message = models.TextField()

    notification_type = models.CharField(max_length=100)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES,default="email")

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts_app.models import OtpVerification
from django.conf import  settings


@receiver(post_save, sender=OtpVerification)
def send_otp_email(sender,instance,created,**kwargs):
    if created:
        send_mail(
            subject="Forgot password OTP",
            message=f"Your otp is {instance.otp}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.user.email],
            fail_silently=False
        )
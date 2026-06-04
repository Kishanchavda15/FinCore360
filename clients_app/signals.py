import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings

from .models import ClientProfile


def generate_password(dob, email):
    symbols = ['@', '#']

    email_part = email.split("@")[0].lower()
    symbol = random.choice(symbols)
    birth_year = dob.year if dob else random.randint(2000, 2010)

    return f"{email_part}{symbol}{birth_year}"


@receiver(post_save, sender=ClientProfile)
def create_client_password(sender, instance, created, **kwargs):
    if created and not instance.password:
        raw_password = generate_password(instance.date_of_birth, instance.email)

        # store hashed password

        hashed_password = make_password(raw_password)
        ClientProfile.objects.filter(id=instance.id).update(
            password=hashed_password
        )

        # send email
        send_mail(
            subject="Your Client Account Password",
            message=f"""
Hello {instance.full_name},

Your account has been created.

Email: {instance.email}
Password: {raw_password}

Please change your password after login.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            fail_silently=False
        )

        #
        # recipient_list = [instance.user.email],
        # fail_silently = False

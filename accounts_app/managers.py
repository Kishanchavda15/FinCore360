from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_field):
        if not email:
            raise ValueError("email is required")  # FIXED

        if not password:
            raise ValueError("password is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password,**extra_field):
        extra_field.setdefault("is_staff", True)
        extra_field.setdefault("is_superuser",True)
        extra_field.setdefault("role", "admin")
        return self.create_user(email,password,**extra_field)
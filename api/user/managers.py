from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.contrib.auth.hashers import make_password

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("Telfon raqam kiritlmagan!")
        user = self.model(
            phone_number = phone_number,
            password = make_password(password),
            **extra_fields
        )
        user.save(using = self._db)
        return user
    
    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            phone_number=phone_number,
            password=password,
            **extra_fields
        )
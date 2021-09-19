import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (BaseUserManager, AbstractUser)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, phone, type, password=None):
        if username is None:
            raise TypeError('Users must have a username.')

        if phone is None:
            raise TypeError('Users must have a phone number.')

        if type is None:
            raise TypeError('Users must have a type.')

        user = self.model(
            username=username,
            phone=phone,
            type=type
        )
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):

    objects = UserManager()

    class Types(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        RESTAURATEUR = 'RESTAURATEUR', 'Restaurateur'
        COURIER = 'COURIER', 'Courier'

    type = models.CharField(
        max_length=50,
        choices=Types.choices,
        blank=True,
        default=None,
        null=True,
        verbose_name="User type"
    )
    phone = models.CharField(
        max_length=12,
        verbose_name='Phone number'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token

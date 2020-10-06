import uuid
from django.db import models
from django.contrib.postgres import fields as postgres
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils.timezone import now


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        return user

    def create_user(self, email, password):
        user = self._create_user(email, password)
        user.save()
        return user

    # utilize the 'createsuperuser' manage.py command to create a user account

    def create_superuser(self, email, password):
        user = self._create_user(email, password)
        user.save()
        return user


class User(AbstractBaseUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    email = postgres.CIEmailField(unique=True)
    active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return str(self.id)

    def update_last_login(self):
        self.last_login = now()
        self.save(update_fields=['last_login'])

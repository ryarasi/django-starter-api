from django.contrib.postgres.fields import ArrayField
from django.db.models.deletion import PROTECT
from common.utils import random_number_with_N_digits, generate_otp
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.fields import CharField, IntegerField
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings
# from django.db.models import JSONField

class LowercaseEmailField(models.EmailField):
    """
    Override EmailField to convert emails to lowercase before saving.
    """
    def to_python(self, value):
        """
        Convert email to lowercase.
        """
        value = super(LowercaseEmailField, self).to_python(value)
        # Value can be None so check that it's a string before lowercasing.
        if isinstance(value, str):
            return value.lower()
        return value


class User(AbstractUser):
    name = models.CharField(max_length=100, default='Uninitialized User')
    email = LowercaseEmailField(blank=False, max_length=255, unique=True)
    avatar = models.CharField(max_length=250, blank=True,
                              null=True, default=settings.DEFAULT_AVATARS['USER'])
    role = models.ForeignKey(
        'UserRole', on_delete=models.PROTECT, blank=True, null=True)
    title = models.CharField(max_length=150, blank=True, null=True)
    bio = models.CharField(max_length=300, blank=True, null=True)

    class StatusChoices(models.TextChoices):
        UNINITIALIZED = 'UI', _('UNINITIALIZED')
        PENDINIG = "PE", _('PENDIING')
        APPROVED = "AP", _('APPROVED')
        SUSPENDED = "SU", _('SUSPENDED')
    # End of Type Choices

    membership_status = models.CharField(
        max_length=2, choices=StatusChoices.choices, default=StatusChoices.UNINITIALIZED)
    searchField = models.CharField(max_length=600, blank=True, null=True)
    last_active = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return f'{self.name}' 

class EmailOTP(models.Model):
    email = LowercaseEmailField(blank=False, max_length=255)
    def generate_otp():
        return generate_otp()
    otp = models.CharField(max_length=10, validators=[
                                  MinLengthValidator(10)], unique=True, default=generate_otp)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class UserRole(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    description = models.CharField(max_length=500,)
    priority = models.IntegerField() # Lower the number higher the priority

    def default_permissions():
        return {}
    permissions = JSONField(default=default_permissions)
    searchField = models.CharField(max_length=600, blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}' 

# For file uploads


class File(models.Model):
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.file.name
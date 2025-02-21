from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from .validations import validate_length


class UserModel(AbstractUser):
    contact = models.PositiveIntegerField(
        validators=[validate_length, MaxValueValidator(9999999999)], null=True, blank=True)
    is_doctor = models.BooleanField(default=False)
    specialist = models.CharField(max_length=250, null=True, blank=True)
    study = models.CharField(max_length=150, null=True, blank=True)

    def __str__(self):
        return self.username

from random import choices
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """Custom User Model"""

    MALE = 'MALE'
    FEMALE = 'FEMALE'
    OTHER = 'OTHER'

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    RU = 'ru'
    EN = 'en'
    LANGUAGE_CHOICES = (
        (RU, 'Russian'),
        (EN, 'English'),
    )

    RUB = 'rub'
    USD = 'usd'
    CURRENCY_CHOICES = (
        (RUB, 'RUB'),
        (USD, 'USD'),
    )

    bio = models.TextField(default='', blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER_CHOICES)
    avatar = models.ImageField(null=True, blank=True)
    birthday = models.DateField(null=True)
    currency = models.CharField(max_length=3, null=True, blank=True, choices=CURRENCY_CHOICES)
    language = models.CharField(max_length=2, null=True, blank=True, choices=LANGUAGE_CHOICES)
    superhost = models.BooleanField(default=False)

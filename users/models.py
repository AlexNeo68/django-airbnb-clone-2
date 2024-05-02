import uuid
from random import choices
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from config import settings


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

    LOGIN_EMAIL = 'LOGIN_EMAIL'
    LOGIN_GITHUB = 'LOGIN_GITHUB'
    LOGIN_KAKAO = 'LOGIN_KAKAO'
    LOGIN_CHOICES = (
        (LOGIN_EMAIL, 'Login Email'),
        (LOGIN_GITHUB, 'Login Github'),
        (LOGIN_KAKAO, 'Login Kakao'),
    )

    bio = models.TextField(default='', blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True, choices=GENDER_CHOICES)
    avatar = models.ImageField(null=True, blank=True, upload_to='avatars')
    birthday = models.DateField(null=True)
    currency = models.CharField(max_length=3, null=True, blank=True, choices=CURRENCY_CHOICES)
    language = models.CharField(max_length=2, null=True, blank=True, choices=LANGUAGE_CHOICES)
    superhost = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=120, default='', blank=True)
    login_type = models.CharField(max_length=20, null=True, blank=True, choices=LOGIN_CHOICES, default=LOGIN_EMAIL)

    def verify_email(self):
        if self.email_verified is False:
            secret = uuid.uuid4().hex[:20]
            self.email_secret = secret
            html_message = render_to_string('emails/verify.html', {'secret': secret})
            send_mail(
                'Email Verified',
                strip_tags(html_message),
                settings.EMAIL_FROM,
                [self.email],
                fail_silently=True,
                html_message=html_message
            )
            self.save()
        return

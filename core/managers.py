from django.contrib.auth.models import UserManager
from django.db import models


class CustomManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class CustomUserManager(CustomManager, UserManager):
    pass

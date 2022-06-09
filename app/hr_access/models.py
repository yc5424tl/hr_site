from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(verbose_name="Avatar Image", upload_to="user_avatar", null=True, blank=True)

# Create your models here.

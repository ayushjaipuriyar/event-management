from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=(
        ('admin', 'Admin'), ('participant', 'Participant')))

# Create your models here.

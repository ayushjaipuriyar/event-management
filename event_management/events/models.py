from django.db import models
from django.contrib.auth import get_user_model
from venues.models import Venue

User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    start_time = models.DateTimeField(default=None)
    end_time = models.DateTimeField(default=None)
    capacity = models.PositiveIntegerField(default=0)
    categories = models.CharField(max_length=100)
    tags = models.CharField(max_length=100)
    creator = models.CharField(max_length=150, default=None)
    venue = models.ForeignKey(
        Venue, on_delete=models.CASCADE, to_field='name', default=None)


class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')
    ])

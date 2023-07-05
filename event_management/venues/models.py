# venues/models.py
from django.db import models


class Venue(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    amenities = models.TextField()

    def __str__(self):
        return self.name
    # Add any other fields or methods specific to the Venue model

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count

import uuid

from django.contrib.auth.models import User

class Property(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Hotel = models.TextField(null=True, blank=True)  # Hotel name
    Category = models.TextField(null=True, blank=True)  # Hotel category
    Rating = models.FloatField(null=True, blank=True)  # Rating of the hotel
    Address = models.TextField(null=True, blank=True)  # Address of the hotel
    Contact = models.TextField(null=True, blank=True)  # Contact information
    Price = models.TextField(null=True, blank=True)  # Price in the string format
    Amenities = models.TextField(null=True, blank=True)  # Amenities provided by the hotel
    Image_URL = models.TextField(null=True, blank=True)  # URL of the image
    Location = models.TextField(null=True, blank=True)  # Location of the hotel
    Page_URL = models.TextField(null=True, blank=True)  # URL to the hotel's page

    @property
    def average_rating(self):
        avg_rating = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating is not None else 0.0

#
    @property
    def rating_count(self):
        return self.ratings.aggregate(Count('id'))['id__count'] or 0
    

    def __str__(self):
        return self.title

class Booking(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.property.title} by {self.guest.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('guest', 'Guest'), ('host', 'Host')], default='guest')

    def __str__(self):
        return self.user.username




class propRating(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="main_ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # Rating out of 5
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('property', 'user')  # A user can only rate a property once

    def __str__(self):
        return f"{self.user.username}'s rating for {self.property.title}"

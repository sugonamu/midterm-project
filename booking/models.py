from django.db import models
from django.contrib.auth.models import User  # Make sure to import the User model




class Hotel(models.Model):
    Hotel = models.TextField(null=True, blank=True)  # Hotel name
    Category = models.TextField(null=True, blank=True)  # Hotel category
    Address = models.TextField(null=True, blank=True)  # Address of the hotel
    Contact = models.TextField(null=True, blank=True)  # Contact information
    Price = models.TextField(null=True, blank=True)  # Price in string format
    Amenities = models.TextField(null=True, blank=True)  # Amenities provided by the hotel
    Image_URL = models.TextField(null=True, blank=True)  # URL of the image
    Location = models.TextField(null=True, blank=True)  # Location of the hotel
    Page_URL = models.TextField(null=True, blank=True)  # URL to the hotel's page

    def __str__(self):
        return self.Hotel or 'Unknown Hotel'

    @property
    def average_rating(self):
        ratings = self.booking_ratings.all()
        if ratings:
            return sum(rating.rating for rating in ratings) / ratings.count()
        return 0.0  # Default to 0.0 if there are no ratings

    @property
    def rating_count(self):
        return self.booking_ratings.count()

class Rating(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="booking_ratings")  # Link to Hotel
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    rating = models.PositiveIntegerField()  # Rating out of 5
    review = models.TextField(blank=True, null=True)  # Optional review
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of rating creation

    class Meta:
        unique_together = ('hotel', 'user')  # A user can only rate a hotel once

    def __str__(self):
        return f"{self.user.username}'s rating for {self.hotel.Hotel}"

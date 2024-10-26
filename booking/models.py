from django.db import models

class Hotel(models.Model):
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

    def __str__(self):
        return self.Hotel or 'Unknown Hotel'

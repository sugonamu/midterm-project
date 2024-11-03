import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from booking.models import Hotel
import uuid
from django.contrib.auth.models import User

class Property(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Hotel = models.TextField(null=True, blank=True)  # Hotel name
    Category = models.TextField(null=True, blank=True)  # Hotel category
    Address = models.TextField(null=True, blank=True)  # Address of the hotel
    Contact = models.TextField(null=True, blank=True)  # Contact information
    Price = models.TextField(null=True, blank=True)  # Price in string format
    Amenities = models.TextField(null=True, blank=True)  # Amenities provided by the hotel
    Image_URL = models.TextField(null=True, blank=True)  # URL of the image
    Location = models.TextField(null=True, blank=True)  # Location of the hotel
    Page_URL = models.TextField(null=True, blank=True)  # URL to the hotel's page

    @property
    def average_rating(self):
        avg_rating = self.main_ratings.aggregate(Avg('rating'))['rating__avg']
        return avg_rating if avg_rating is not None else 0.0

    @property
    def rating_count(self):
        return self.main_ratings.aggregate(Count('id'))['id__count'] or 0

    def save(self, *args, **kwargs):
        # Try to get the existing Hotel instance based on the hotel name
        hotel_instance = Hotel.objects.filter(Hotel=self.Hotel).first()

        if hotel_instance is None:
            # If the hotel does not exist, create a new one
            hotel_instance = Hotel.objects.create(
                Hotel=self.Hotel,
                Category=self.Category,
                Address=self.Address,
                Contact=self.Contact,
                Price=self.Price,
                Amenities=self.Amenities,
                Image_URL=self.Image_URL,
                Location=self.Location,
                Page_URL=self.Page_URL,
            )
        else:
            # If the hotel already exists, update its details
            hotel_instance.Category = self.Category
            hotel_instance.Address = self.Address
            hotel_instance.Contact = self.Contact
            hotel_instance.Price = self.Price
            hotel_instance.Amenities = self.Amenities
            hotel_instance.Image_URL = self.Image_URL
            hotel_instance.Location = self.Location
            hotel_instance.Page_URL = self.Page_URL
            hotel_instance.save()  # Save the updated hotel instance

        super().save(*args, **kwargs)  # Save the property instance

    def delete(self, *args, **kwargs):
        # Get the associated Hotel instance and delete it
        hotel_instance = Hotel.objects.filter(Hotel=self.Hotel).first()
        if hotel_instance:
            hotel_instance.delete()  # Delete the associated hotel instance
        
        super().delete(*args, **kwargs)  # Delete the property instance

    def __str__(self):
        return self.Hotel or 'Unknown Property'


# Rest of your models remain unchanged

    
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

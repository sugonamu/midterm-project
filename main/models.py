from django.db import models
from django.contrib.auth.models import User
import uuid

class Property(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.CharField(max_length=255)
    number_of_guests = models.IntegerField()
    number_of_bedrooms = models.IntegerField()
    number_of_bathrooms = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
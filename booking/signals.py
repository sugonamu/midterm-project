from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from main.models import Property  # Import Property from the main app
from .models import Hotel  # Import Hotel from the booking app

@receiver(post_save, sender=Property)
def create_hotel(sender, instance, created, **kwargs):
    if created:  # Only create hotel if a property is newly created
        # Use transaction to ensure atomicity
        with transaction.atomic():
            Hotel.objects.create(
                Hotel=instance.Hotel,  # Use the correct field for hotel name
                Category=instance.Category,  # Map the category correctly
                Rating=instance.Rating,  # Map rating if it exists
                Address=instance.Address,  # Map address
                Contact=instance.Contact,  # Map contact
                Price=instance.Price,  # Keep price as is
                Amenities=instance.Amenities,  # Map amenities
                Image_URL=instance.Image_URL,  # Map image URL
                Location=instance.Location,  # Map location
                Page_URL=instance.Page_URL  # Map page URL
            )

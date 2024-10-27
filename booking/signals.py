from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from django.core.exceptions import ValidationError
from main.models import Property  
from .models import Hotel  

@receiver(post_save, sender=Property)
def create_hotel(sender, instance, created, **kwargs):
    if created:  # Only create hotel if a property is newly created
        try:
            with transaction.atomic():
                Hotel.objects.create(
                    hotel_name=instance.hotel_name,
                    category=instance.category,
                    address=instance.address,
                    contact=instance.contact,
                    price=instance.price,
                    amenities=instance.amenities,
                    image_url=instance.image_url,
                    location=instance.location,
                    page_url=instance.page_url
                )
        except ValidationError as e:
            print(f"Error creating Hotel: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

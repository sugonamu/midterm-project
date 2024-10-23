from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])


class HotelManager(models.Manager):
    def get_queryset(self):
        return super(HotelManager, self).get_queryset().filter(is_active=True)


class Hotel(models.Model):
    page_url = models.URLField(max_length=500, blank=True)  # <-- Add this field for the page URL
    title = models.CharField(max_length=255)  # This would correspond to the "Hotel" field
    category = models.ForeignKey(Category, related_name='hotels', on_delete=models.CASCADE)
    address = models.TextField(blank=True)  # Corresponding to "Address" field
    contact = models.CharField(max_length=255, blank=True)  # Corresponding to "Contact" field
    price = models.CharField(max_length=50)  # Corresponding to "Price" field (stored as string for now)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, help_text="Rating from 1.0 to 5.0")
    amenities = models.TextField(blank=True)  # Corresponding to "Amenities" field
    location = models.CharField(max_length=255)  # Corresponding to "Location" field
    image_url = models.URLField(max_length=500, blank=True)  # Corresponding to "Image_URL" field
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    hotels = HotelManager()

    class Meta:
        verbose_name_plural = 'Hotels'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store:hotel_detail", args=[self.slug])

from rest_framework import serializers
from .models import Property

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'Hotel', 'Category', 'Address', 'Contact', 'Price', 'Amenities', 'Image_URL', 'Location', 'Page_URL']

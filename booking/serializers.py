from rest_framework import serializers
from .models import Hotel, Rating

class HotelSerializer(serializers.ModelSerializer):
    # No need to specify source since we have annotated fields from the queryset
    avg_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Hotel
        fields = [
            'id', 'Hotel', 'Category', 'Address', 'Contact', 'Price', 'Amenities',
            'Image_URL', 'Location', 'Page_URL', 'avg_rating', 'review_count'
        ]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'hotel', 'user', 'rating', 'review', 'created_at']

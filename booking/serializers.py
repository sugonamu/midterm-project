from rest_framework import serializers
from .models import Hotel, Rating

class RatingSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Rating
        fields = ['user', 'rating', 'review', 'created_at']

    def get_user(self, obj):
        return {"username": obj.user.username}

class HotelSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    review_count = serializers.IntegerField(read_only=True)
    ratings = RatingSerializer(many=True, read_only=True, source='booking_ratings')

    class Meta:
        model = Hotel
        fields = [
            'id', 'Hotel', 'Category', 'Address', 'Contact', 'Price', 'Amenities',
            'Image_URL', 'Location', 'Page_URL', 'avg_rating', 'review_count', 'ratings'
        ]

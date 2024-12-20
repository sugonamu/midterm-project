from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.core import serializers
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Hotel, Rating
from .serializers import HotelSerializer, RatingSerializer

def proxy_image(request):
    original_url = request.GET.get('url')
    if not original_url:
        return HttpResponse(status=400)

    response = requests.get(original_url, stream=True)
    if response.status_code == 200:
        return HttpResponse(response.content, content_type=response.headers.get('Content-Type'))
    return HttpResponse(status=404)

class HotelList(generics.ListCreateAPIView):
    """
    Lists all hotels with annotated average rating and review count.
    Allows creating a new hotel.
    """
    queryset = Hotel.objects.annotate(
        avg_rating=Avg('booking_ratings__rating'),
        review_count=Count('booking_ratings')
    )
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Adjust permission as needed



class HotelDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific hotel, including reviews.
    """
    queryset = Hotel.objects.annotate(
        avg_rating=Avg('booking_ratings__rating'),
        review_count=Count('booking_ratings')
    ).prefetch_related('booking_ratings__user')  # Prefetch related reviews and users
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
@method_decorator(csrf_exempt, name='dispatch')
class AddRating(APIView):
    def post(self, request, hotel_id):
        hotel = get_object_or_404(Hotel, id=hotel_id)
        serializer = RatingSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(hotel=hotel, user=request.user)
            return Response({'status': 'success', 'message': 'Rating added successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class HotelRatings(generics.ListAPIView):
    """
    Retrieve all ratings for a given hotel.
    """
    serializer_class = RatingSerializer

    def get_queryset(self):
        hotel_id = self.kwargs['hotel_id']
        return Rating.objects.filter(hotel_id=hotel_id).select_related('user', 'hotel')




def get_hotels(request):
    # Direct JSON serialization of hotels
    data = Hotel.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")


def clean_price(price_str):
    # Consider storing Price as a numeric field in the database for better performance
    cleaned_price = price_str.replace('Rp', '').replace('.', '').strip()
    return int(cleaned_price)


def hotel_search(request):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'asc')

    # If you can't change the database schema, you still have to do this in Python
    # Otherwise, convert Price to a numeric field and use order_by in queryset.
    hotels = Hotel.objects.all()

    if query:
        hotels = hotels.filter(Hotel__icontains=query) | hotels.filter(Location__icontains=query)

    # Annotate average rating and review count
    hotels = hotels.annotate(
        avg_rating=Avg('booking_ratings__rating'),
        review_count=Count('booking_ratings')
    )

    # Convert to a list for Python-based sorting
    hotels_list = list(hotels)
    if sort_by == 'desc':
        hotels_list.sort(key=lambda x: clean_price(x.Price), reverse=True)
    else:
        hotels_list.sort(key=lambda x: clean_price(x.Price))

    # If AJAX, return JSON data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        hotels_data = [
            {
                'id': hotel.id,
                'Hotel': hotel.Hotel,
                'Price': hotel.Price,
                'avg_rating': hotel.avg_rating or 'Not Rated',
                'review_count': hotel.review_count,
                'Image_URL': hotel.Image_URL,
            }
            for hotel in hotels_list
        ]
        return JsonResponse({'hotels': hotels_data})

    # Render the full page for non-AJAX requests
    return render(request, 'booking/hotel_search.html', {'hotels': hotels_list, 'sort_by': sort_by})


@login_required
def book_hotel(request, hotel_id):
    # Ensure user is logged in to book hotel
    hotel = get_object_or_404(Hotel, id=hotel_id)
    amenities_list = hotel.Amenities.split(',')
    related_hotels = Hotel.objects.filter(Location=hotel.Location).exclude(id=hotel.id)
    ratings = hotel.booking_ratings.select_related('user').all()  # Prefetch ratings

    return render(request, 'booking/book_hotel.html', {
        'hotel': hotel,
        'amenities_list': amenities_list,
        'related_hotels': related_hotels,
        'ratings': ratings
    })


def booking_success(request):
    return render(request, 'booking/booking_success.html')


@login_required
def add_rating(request, hotel_id):
    hotel_instance = get_object_or_404(Hotel, pk=hotel_id)

    # Check if the user has already rated this hotel
    existing_rating = Rating.objects.filter(hotel=hotel_instance, user=request.user).first()

    if request.method == "POST":
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review')

        # Validate rating value
        try:
            rating_value = int(rating_value)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid rating value")

        if existing_rating:
            # Update existing rating
            existing_rating.rating = rating_value
            existing_rating.review = review_text
            existing_rating.save()
        else:
            # Create a new rating
            Rating.objects.create(
                hotel=hotel_instance,
                user=request.user,
                rating=rating_value,
                review=review_text
            )

        # Redirect to hotel detail page
        return redirect('booking:book_hotel', hotel_id=hotel_instance.id)

    # GET request: render the rating form
    return render(request, 'booking/add_rating.html', {
        'hotel': hotel_instance,
        'existing_rating': existing_rating
    })


def show_json(request):
    # Fetch all ratings and serialize
    ratings = Rating.objects.select_related('hotel', 'user').all()
    data = serializers.serialize('json', ratings)
    return HttpResponse(data, content_type='application/json')

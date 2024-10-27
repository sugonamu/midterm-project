from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.core import serializers
from .models import Hotel,Rating
from django.db.models import Avg,Count
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest

def get_hotels(request):
    data = Hotel.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def clean_price(price_str):
    # Remove "Rp" and commas, and convert to integer for proper sorting
    cleaned_price = price_str.replace('Rp', '').replace('.', '').strip()
    return int(cleaned_price)

def hotel_search(request):
    query = request.GET.get('q', '')  # Get the search query
    sort_by = request.GET.get('sort', 'asc')  # Get the sorting order, default to 'asc'

    if query:
        hotels = Hotel.objects.filter(
            Hotel__icontains=query  # Use "Hotel" field for searching the hotel name
        ) | Hotel.objects.filter(
            Location__icontains=query  # Use "Location" field for searching the location
        )
    else:
        hotels = Hotel.objects.all()  # Show all hotels if no query
    
    # Annotate average rating and count of ratings
    hotels = hotels.annotate(
        avg_rating=Avg('booking_ratings__rating'),  # Average rating
        review_count=Count('booking_ratings')  # Count of reviews
    )


    # Sort by price
    hotels = list(hotels)  # Convert queryset to a list to allow sorting with custom logic
    if sort_by == 'desc':
        hotels.sort(key=lambda x: clean_price(x.Price), reverse=True)  # Sort in descending order
    else:
        hotels.sort(key=lambda x: clean_price(x.Price))  # Sort in ascending order

    # Check if the request is AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        hotels_data = [
            {
                'id': hotel.id,
                'Hotel': hotel.Hotel,
                'Price': hotel.Price,
                'Rating': hotel.Rating,
                'Image_URL': hotel.Image_URL,
                'Location': hotel.Location,
                'Page_URL': hotel.Page_URL,
            }
            for hotel in hotels
        ]
        return JsonResponse({'hotels': hotels_data})

    # Render the full page if not AJAX
    return render(request, 'booking/hotel_search.html', {'hotels': hotels, 'sort_by': sort_by})

# Booking view (assuming a simple booking model)
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)
    
    # Split amenities by commas
    amenities_list = hotel.Amenities.split(',')

    # Get related hotels by location (excluding the current hotel)
    related_hotels = Hotel.objects.filter(Location=hotel.Location).exclude(id=hotel.id)

    # Fetch the ratings for the current hotel
    ratings = hotel.booking_ratings.all()  # This accesses the related ratings using the related_name

    return render(request, 'booking/book_hotel.html', {
        'hotel': hotel,
        'amenities_list': amenities_list,  # Pass the split amenities list to the template
        'related_hotels': related_hotels,
        'ratings': ratings  # Pass the ratings to the template
    })

def booking_success(request):
    return render(request, 'booking/booking_success.html')





def add_rating(request, hotel_id):
    hotel_instance = get_object_or_404(Hotel, pk=hotel_id)
    
    # Check if the user has already rated this hotel
    existing_rating = Rating.objects.filter(hotel=hotel_instance, user=request.user).first()
    
    if request.method == "POST":
        rating_value = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        # Ensure rating_value is a number
        try:
            rating_value = int(rating_value)
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid rating value")

        if existing_rating:
            # Update the existing rating
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

        # Redirect to the hotel detail page after adding/updating the rating
        return redirect('booking:book_hotel', hotel_id=hotel_instance.id)  # Adjust URL as necessary

    # If GET request, render the rating form
    return render(request, 'booking/add_rating.html', {
        'hotel': hotel_instance,
        'existing_rating': existing_rating
    })

from django.urls import path
from . import booking_views

app_name = 'booking'

urlpatterns = [
    path('',booking_views.hotel_search,name='hotel_search'),
    path('book/<int:hotel_id>/', booking_views.book_hotel, name='book_hotel'),
    path('booking/success/', booking_views.booking_success, name='booking_success'),  # Success page after booking
    path('hotel/<int:hotel_id>/add-rating/', booking_views.add_rating, name='add_rating'),
    path('ratings/json/', booking_views.show_json, name='show_json'),
    path('api/hotels/', booking_views.HotelList.as_view(), name='hotel-list'),
    path('api/hotels/<int:pk>/', booking_views.HotelDetail.as_view(), name='hotel-detail'),
    path('api/hotels/<int:hotel_id>/ratings/', booking_views.HotelRatings.as_view(), name='hotel-ratings'),
    path('api/hotels/<int:hotel_id>/add-rating/', booking_views.AddRating.as_view(), name='add-rating'),
]


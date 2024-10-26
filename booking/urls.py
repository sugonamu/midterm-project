from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path("",views.get_hotels,name="get_hotels"),
    path('search/', views.hotel_search, name='hotel_search'),
    path('book/<int:hotel_id>/', views.book_hotel, name='book_hotel'),
    path('booking/success/', views.booking_success, name='booking_success'),  # Success page after booking
]

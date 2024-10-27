# payment/urls.py
from django.urls import path
from .payment_views import payment_page

app_name = 'payment'

urlpatterns = [
    path('<int:hotel_id>/', payment_page, name='payment_page'),
    
]

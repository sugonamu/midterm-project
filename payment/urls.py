from django.urls import path
from payment.views import payment_page

app_name = 'payment'

urlpatterns = [
    path('', payment_page, name='payment_page'),
]   
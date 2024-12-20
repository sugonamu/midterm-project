from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .payment_views import payment_page, PaymentProfileViewSet, TransactionViewSet, process_payment

app_name = 'payment'

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'payment-profiles', PaymentProfileViewSet, basename='paymentprofile')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('<int:hotel_id>/', payment_page, name='payment_page'),
    path('api/', include(router.urls)),  
]

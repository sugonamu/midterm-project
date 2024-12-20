from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, PaymentProfile, STATUS_TRANSACTION_PAID, PAYMENT_METHOD_CREDIT_CARD
from booking.models import Hotel
from rest_framework import viewsets
from .serializers import PaymentProfileSerializer, TransactionSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@login_required
def payment_page(request, hotel_id):
    hotel = Hotel.objects.get(id=hotel_id)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        credit_card_number = request.POST.get('credit_card_number')
        valid_thru = request.POST.get('valid_thru')
        cvv = request.POST.get('cvv')
        card_name = request.POST.get('card_name')
        booking_date = request.POST.get('booking_date')

        # Save Credit Card Transaction~
        transaction = Transaction(
            user=request.user,
            hotel=hotel,
            total_price=parse_rupiah_string_to_float(hotel.Price),  # Example total price
            phone_number= mobile_number,  # Example phone number
            credit_card_number=credit_card_number,
            valid_thru=valid_thru,
            cvv=cvv,
            card_name=card_name,
            booking_date = booking_date,
            payment_method=PAYMENT_METHOD_CREDIT_CARD,
            status=STATUS_TRANSACTION_PAID
        )
        transaction.save()

        return render(request, 'payment_success.html', {
            "full_name" : full_name, 
            "email" : email, 
            "mobile_number" : mobile_number, 
            "credit_card_number" : credit_card_number, 
            "valid_thru" : valid_thru, 
            "cvv" : cvv, 
            "card_name" : card_name, 
            "booking_date" : booking_date,
            "status" : transaction.status,
            })
    
    return render(request, "payment.html", {
        "Price": hotel.Price,
        "Hotel": hotel.Hotel,
        "Category": hotel.Category,
        "Amenities": hotel.Amenities,
        "City": hotel.Location,
        "Address": hotel.Address,

    })

def parse_rupiah_string_to_float(rupiah_string):
    return float(rupiah_string.replace('Rp', '').replace('.', '').replace(',', '.'))

class PaymentProfileViewSet(viewsets.ModelViewSet):
    queryset = PaymentProfile.objects.all()
    serializer_class = PaymentProfileSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

def payment_profile(request):
    return render(request, 'payment_profile.html')

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        phone_number = data.get('phone_number')
        credit_card_number = data.get('credit_card_number')
        valid_thru = data.get('valid_thru')
        cvv = data.get('cvv')
        card_name = data.get('card_name')

        # Process the payment here
        # For demonstration, let's assume the payment is always successful
        response_data = {
            'status': 'success',
            'message': 'Payment processed successfully'
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

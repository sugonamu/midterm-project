from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, PaymentProfile, STATUS_TRANSACTION_PAID, PAYMENT_METHOD_CREDIT_CARD
from booking.models import Hotel
from rest_framework import viewsets
from .serializers import PaymentProfileSerializer, TransactionSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User

def parse_rupiah_string_to_float(rupiah_string):
    # Remove the currency prefix
    clean_str = rupiah_string.replace('Rp', '')
    
    # Remove Unicode non-breaking spaces and 'Â' characters
    clean_str = clean_str.replace('Â', '').replace('\xa0', '')
    
    # Remove thousand separators ('.')
    clean_str = clean_str.replace('.', '')
    
    # Replace commas with dots for decimals, if needed
    clean_str = clean_str.replace(',', '.')
    
    # Strip any remaining whitespace
    clean_str = clean_str.strip()
    
    # Convert to float
    return float(clean_str)

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
        mobile_number = request.POST.get('mobile_number')
        credit_card_number = request.POST.get('credit_card_number')
        valid_thru = request.POST.get('valid_thru')
        cvv = request.POST.get('cvv')
        card_name = request.POST.get('card_name')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        booking_date = request.POST.get('booking_date')
        hotel_id = request.POST.get('hotel_id')
        hotel = Hotel.objects.get(id=hotel_id)
        price_str = request.POST.get('price')
        price = parse_rupiah_string_to_float(price_str)

        # Save the transaction
        transaction = Transaction(
            user=request.user if request.user.is_authenticated else None,
            hotel=hotel,
            booking_date=booking_date,
            total_price=price,
            phone_number=mobile_number,
            credit_card_number=credit_card_number,
            valid_thru=valid_thru,
            cvv=cvv,
            card_name=card_name,
            payment_method=PAYMENT_METHOD_CREDIT_CARD,
            status=STATUS_TRANSACTION_PAID
        )
        transaction.save()
        response_data = {
            'status': 'success',
            'message': 'Payment processed successfully',
            'transaction_id': transaction.id
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

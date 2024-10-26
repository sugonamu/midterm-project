from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Transaction, PaymentProfile

@login_required
def payment_page(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if payment_method == 'CREDIT_CARD':
            credit_card_number = request.POST.get('credit_card_number')
            valid_thru = request.POST.get('valid_thru')
            cvv = request.POST.get('cvv')
            card_name = request.POST.get('card_name')

            # Save Credit Card Transaction
            transaction = Transaction(
                total_price=100,  # Example total price
                phone_number='123456789',  # Example phone number
                credit_card_number=credit_card_number,
                valid_thru=valid_thru,
                cvv=cvv,
                card_name=card_name,
                payment_method='CREDIT_CARD',
                status='UNPAID'
            )
            transaction.save()

        elif payment_method == 'VIRTUAL_ACCOUNT':
            virtual_account_provider = request.POST.get('virtual_account_provider')

            # Save Virtual Account Transaction
            transaction = Transaction(
                total_price=100,  # Example total price
                phone_number='123456789',  # Example phone number
                credit_card_number='',  # No card details for virtual account
                payment_method='VIRTUAL_ACCOUNT',
                status='UNPAID'
            )
            transaction.save()

        messages.success(request, 'Payment Submitted Successfully!')
        return redirect('payment:payment_page')

    context = {}
    return render(request, "payment.html", context)

from django.db import models
from django.contrib.auth.models import User
from booking.models import Hotel
# Create your models here.

class PaymentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payment_profile')
    phone_number = models.CharField(max_length=255, blank=True)
    credit_card_number = models.CharField(max_length=255, blank=True)
    valid_thru = models.CharField(max_length=5, blank=True)
    cvv = models.CharField(max_length=4, blank=True)
    card_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'payment_profile'
        verbose_name = 'Payment Profile'



STATUS_TRANSACTION_PAID = 'PAID'
STATUS_TRANSACTION_UNPAID = 'UNPAID'
STATUS_TRANSACTION_CHOICES = {
    (STATUS_TRANSACTION_PAID, 'Paid'),
    (STATUS_TRANSACTION_UNPAID, 'Unpaid'),
}

PAYMENT_METHOD_CREDIT_CARD = 'CREDIT_CARD'
PAYMENT_METHOD_VIRTUAL_ACCOUNT = 'VIRTUAL_ACCOUNT'
PAYMENT_METHOD_CHOICES = {
    (PAYMENT_METHOD_CREDIT_CARD, 'Credit Card'),
    (PAYMENT_METHOD_VIRTUAL_ACCOUNT, 'Virtual Account'),
}


class Transaction(models.Model):
# Foreign Key to Booking
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='transactions', blank=True, null=True)
    booking_date = models.DateField(blank = True, null=True)
    total_price =  models.FloatField(default=0)
    phone_number = models.CharField(max_length=255, blank=True)
    credit_card_number = models.CharField(max_length=255, blank=True)
    valid_thru = models.CharField(max_length=5, blank=True)
    cvv = models.CharField(max_length=4, blank=True)
    card_name = models.CharField(max_length=255, blank=True)
    payment_method = models.CharField(max_length=255, default=PAYMENT_METHOD_CREDIT_CARD, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=255, default=STATUS_TRANSACTION_UNPAID, choices=STATUS_TRANSACTION_CHOICES)

    class Meta:
        db_table = 'transaction'
        verbose_name = 'Transaction'
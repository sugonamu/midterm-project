from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Transaction

User = get_user_model()

class PaymentPageTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_credit_card_payment_submission(self):
        # Define the credit card payment data
        credit_card_data = {
            'payment_method': 'CREDIT_CARD',
            'credit_card_number': '1234567812345678',
            'valid_thru': '12/25',
            'cvv': '123',
            'card_name': 'Test User'
        }

        # Send POST request with credit card data
        response = self.client.post(reverse('payment:payment_page'), credit_card_data)
        
        # Check if the response redirects to the payment page
        self.assertRedirects(response, reverse('payment:payment_page'))

        # Verify that the transaction was created in the database
        transaction = Transaction.objects.get(payment_method='CREDIT_CARD')
        self.assertEqual(transaction.total_price, 100)
        self.assertEqual(transaction.phone_number, '123456789')
        self.assertEqual(transaction.credit_card_number, '1234567812345678')
        self.assertEqual(transaction.valid_thru, '12/25')
        self.assertEqual(transaction.cvv, '123')
        self.assertEqual(transaction.card_name, 'Test User')
        self.assertEqual(transaction.status, 'UNPAID')

        # Verify that a success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Payment Submitted Successfully!" in str(message) for message in messages))

    def test_virtual_account_payment_submission(self):
        # Define the virtual account payment data
        virtual_account_data = {
            'payment_method': 'VIRTUAL_ACCOUNT',
            'virtual_account_provider': 'Example Bank'
        }

        # Send POST request with virtual account data
        response = self.client.post(reverse('payment:payment_page'), virtual_account_data)

        # Check if the response redirects to the payment page
        self.assertRedirects(response, reverse('payment:payment_page'))

        # Verify that the transaction was created in the database
        transaction = Transaction.objects.get(payment_method='VIRTUAL_ACCOUNT')
        self.assertEqual(transaction.total_price, 100)
        self.assertEqual(transaction.phone_number, '123456789')
        self.assertEqual(transaction.credit_card_number, '')
        self.assertEqual(transaction.status, 'UNPAID')

        # Verify that a success message was added
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Payment Submitted Successfully!" in str(message) for message in messages))

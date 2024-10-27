from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from booking.models import Hotel
from payment.models import Transaction, STATUS_TRANSACTION_PAID, PAYMENT_METHOD_CREDIT_CARD
from payment.payment_views import parse_rupiah_string_to_float

class PaymentPageTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.hotel = Hotel.objects.create(
            id=1,
            Price='Rp1.000.000',
            Hotel='Test Hotel',
            Category='Luxury',
            Rating=5,
            Amenities='Pool, Gym, Spa',
            Location='Test City',
            Address='123 Test Street'
        )
        self.url = reverse('payment_page', args=[self.hotel.id])

    def test_payment_page_get(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment.html')
        self.assertContains(response, self.hotel.Price)
        self.assertContains(response, self.hotel.Hotel)

    def test_payment_page_post(self):
        self.client.login(username='testuser', password='12345')
        post_data = {
            'full_name': 'Test User',
            'email': 'testuser@example.com',
            'mobile_number': '1234567890',
            'credit_card_number': '4111111111111111',
            'valid_thru': '12/23',
            'cvv': '123',
            'card_name': 'Test User',
            'booking_date': '2023-10-10'
        }
        response = self.client.post(self.url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment_success.html')
        self.assertTrue(Transaction.objects.filter(user=self.user, hotel=self.hotel).exists())
        transaction = Transaction.objects.get(user=self.user, hotel=self.hotel)
        self.assertEqual(transaction.total_price, parse_rupiah_string_to_float(self.hotel.Price))
        self.assertEqual(transaction.phone_number, post_data['mobile_number'])
        self.assertEqual(transaction.credit_card_number, post_data['credit_card_number'])
        self.assertEqual(transaction.valid_thru, post_data['valid_thru'])
        self.assertEqual(transaction.cvv, post_data['cvv'])
        self.assertEqual(transaction.card_name, post_data['card_name'])
        self.assertEqual(transaction.booking_date, post_data['booking_date'])
        self.assertEqual(transaction.payment_method, PAYMENT_METHOD_CREDIT_CARD)
        self.assertEqual(transaction.status, STATUS_TRANSACTION_PAID)
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from main.models import UserProfile

class AuthenticationTests(TestCase):
    def setUp(self):
        # Define URLs
        self.register_url = reverse('main:register')  
        self.login_url = reverse('main:login')        

    def test_user_registration(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'role': 'guest' 
        })
        
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='testuser').exists())
        user = User.objects.get(username='testuser')
        profile = UserProfile.objects.get(user=user)
        self.assertEqual(profile.role, 'guest')
        

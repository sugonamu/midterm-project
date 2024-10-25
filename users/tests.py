from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.urls import reverse

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        # Use `get_or_create` to avoid creating duplicate profiles
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        self.client.login(username='testuser', password='password')

    def test_profile_view_loads_for_logged_in_user(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_profile_update_with_valid_data(self):
        response = self.client.post(reverse('profile'), {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'image': ''  # Add image data if applicable
        })
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after a successful update

        # Refresh the user from the database to check if the username was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')


    def test_profile_update_with_invalid_data(self):
        response = self.client.post(reverse('profile'), {
            'username': '',  # Invalid, username cannot be empty
            'email': 'invalidemail',  # Invalid email format
            'image': ''  # If you have an image, you can pass it here
        })
        self.assertEqual(response.status_code, 200)  # Should reload form due to errors
        self.assertContains(response, 'Please correct the error below.')

    
    def tearDown(self):
        # Clean up after each test
        self.user.delete()
        self.profile.delete()


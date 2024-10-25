from django.urls import path
from .views import profile_view, auto_login_view

urlpatterns = [
    path('profile/', profile_view, name='profile'),  # This line handles the /profile/ URL
    path('auto-login/', auto_login_view, name='auto_login'),  # Add this line

]

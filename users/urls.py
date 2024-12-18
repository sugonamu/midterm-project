from django.urls import path
from .views import UserDetailView, profile_view, show_json, update_profile_flutter, UserProfileView

urlpatterns = [
    path('profile/', profile_view, name='profile'),  
    path('json/', show_json, name='json'), 
    path('update_profile_flutter/', update_profile_flutter, name='update_profile_flutter'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('api', UserProfileView.as_view(), name='user_profile'),  # New endpoint
]

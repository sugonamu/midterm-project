from django.urls import path
from .views import ProfileListView, UserDetailView, profile_view, show_json, update_profile_flutter

urlpatterns = [
    path('profile/', profile_view, name='profile'),  
    path('json/', show_json, name='json'), 
    path('update_profile_flutter/', update_profile_flutter, name='update_profile_flutter'),
    path('profiles/', ProfileListView.as_view(), name='profile-list'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]

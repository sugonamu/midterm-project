from django.urls import path
from .views import profile_view, show_json, update_profile_flutter

urlpatterns = [
    path('profile/', profile_view, name='profile'),  
    path('json/', show_json, name='json'), 
    path('update_profile_flutter/', update_profile_flutter, name='update_profile_flutter'),
]

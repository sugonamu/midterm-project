from django.urls import path
from .views import login, register, logout, edit_property, delete_property

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('editproperty/<uuid:property_id>/', edit_property, name='edit_property'),
    path('delete/<uuid:property_id>/', delete_property, name='delete_property'),
]

from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),  
    path('properties/', views.property_list, name='property_list'),  
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),  
    path('error/', views.error, name='error'),
    path('add_property/', views.add_property, name='add_property'),
    path('properties/<uuid:property_id>/', views.property_detail, name='property_detail'),
    path('edit_property/<uuid:property_id>/', views.edit_property, name='edit_property'),
    path('property/delete/<uuid:property_id>/', views.delete_property, name='delete_property'),
    path('properties/<uuid:property_id>/rate/', views.add_rating, name='add_rating'),
    path('property/<uuid:property_id>/reviews/', views.property_reviews, name='property_reviews'),
    path('host_dashboard/', views.host_dashboard, name='host_dashboard')
]

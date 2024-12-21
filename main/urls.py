from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),  
    path('add_property_django/', views.add_property, name='add_property'),
    path('edit_property/<uuid:property_id>/', views.edit_property, name='edit_property'),
    path('property/delete/<uuid:property_id>/', views.delete_property, name='delete_property'),
    path('host_dashboard/', views.host_dashboard, name='host_dashboard'),
    path('add-property-ajax/', views.add_property_ajax, name='add_property_ajax'),
    path('fetch-properties/', views.fetch_properties, name='fetch_properties'),
    path('user-profiles/', views.all_user_profiles_json, name='all_user_profiles_json'),
    path('add_property/', views.add_property, name='add_property'),
    path('propertylistview/', views.PropertyListView.as_view(), name='propertylistview'),
    path('delete/<uuid:property_id>/', views.delete_property , name = 'delete_property'),
    path('property/<str:property_id>/', views.get_property_details, name='get_property_details'),
    path('edit_property_api/', views.edit_property_api, name='edit_property_api'),
]

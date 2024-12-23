import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import PropertyForm
from .models import Property, UserProfile ,propRating, Booking
from functools import wraps
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.hashers import make_password
import json

def is_host(user):
    return user.is_authenticated and user.userprofile.role == 'host'

def is_guest(user):
    return user.is_authenticated and user.userprofile.role == 'guest'


from django.http import HttpResponseForbidden

def user_is_host(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_host(request.user):
            return HttpResponseForbidden()  # Deny access if not a host
        return view_func(request, *args, **kwargs)
    return _wrapped_view


@user_is_host
def host_dashboard(request):
    properties = request.user.properties.all() 
    bookings = Booking.objects.filter(property__in=properties)
    return render(request, 'host_dashboard.html', {'properties': properties, 'bookings': bookings})


from django.core.exceptions import ValidationError


@user_is_host
@csrf_exempt
@require_POST
def add_property_ajax(request):
    try:
        # Extract fields from the POST request
        Hotel = request.POST.get("Hotel")
        category = request.POST.get("Category")
        rating = request.POST.get("Rating")
        address = request.POST.get("Address")
        contact = request.POST.get("Contact")
        price = request.POST.get("Price")
        amenities = request.POST.get("Amenities")
        image_url = request.POST.get("Image_URL")
        location = request.POST.get("Location")
        page_url = request.POST.get("Page_URL")
        
        # Validate required fields
        required_fields = [Hotel, category, address, contact, price, location]
        if any(field is None or field.strip() == '' for field in required_fields):
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

        # Create a new Property instance
        property_instance = Property(
            host=request.user,
            Hotel=Hotel,
            Category=category,
            Address=address,
            Contact=contact,
            Price=price,
            Amenities=amenities,
            Image_URL=image_url,
            Location=location,
            Page_URL=page_url
        )
        
        # Save the property instance
        property_instance.full_clean()  # Validate model data before saving
        property_instance.save()

        return JsonResponse({'success': True, 'message': 'Property added successfully.'}, status=201)

    except ValidationError as ve:
        # Handle validation errors
        return JsonResponse({'success': False, 'message': str(ve)}, status=400)
    except Exception as e:
        # Catch other exceptions and return a generic error message
        return JsonResponse({'success': False, 'message': 'An error occurred: ' + str(e)}, status=500)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                response = redirect('booking:hotel_search')  # Default redirect

                # Set last login cookie
                response.set_cookie('last_login', str(datetime.datetime.now()))

                # Role-based redirection
                if user.userprofile.role == 'host':
                    return redirect('main:host_dashboard')  # Replace with your host dashboard URL name
                else:
                    return redirect('booking:hotel_search')  # Replace with your guest dashboard URL name

            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        try:
            # Parse JSON request body
            data = json.loads(request.body)
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')
            role = data.get('role')

            # Validate input
            if not username or not password1 or not password2 or not role:
                return JsonResponse({'status': 'error', 'message': 'All fields are required.'}, status=400)

            if password1 != password2:
                return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'}, status=400)

            # Check if the username already exists
            if UserProfile.objects.filter(username=username).exists():
                return JsonResponse({'status': 'error', 'message': 'Username already exists.'}, status=400)

            # Create the User object and set password properly
            user = UserProfile.objects.create_user(username=username, password=password1)

            # Create associated UserProfile with role
            user_profile = UserProfile.objects.create(user=user, role=role)

            # Optionally, you can send a confirmation email or handle further user setup

            return JsonResponse({'status': 'success', 'message': 'Registration successful.'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

def logout(request):
    auth_logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@user_is_host
def add_property_django(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.host = request.user  # Set the host to the logged-in user
            
            try:
                property_instance.save()  # Save the property instance to the database
                return JsonResponse({'success': True, 'message': 'Property added successfully.'})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)})  # Return error if save fails
        else:
            # Return form errors in JSON format
            return JsonResponse({'success': False, 'errors': form.errors.as_json()})

    # Handle GET request by rendering the form
    form = PropertyForm()  # Create a blank form instance
    return render(request, 'addproperty.html', {'form': form})

@user_is_host
def edit_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id, host=request.user)

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('main:host_dashboard')
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, 'editproperty.html', {'form': form})

@user_is_host
def delete_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.delete()
    return HttpResponseRedirect(reverse('main:host_dashboard'))

@user_is_host
def fetch_properties(request):
    if request.method == 'GET':
        properties = Property.objects.all().values('Hotel', 'Category', 'Address', 'Price')  # Add other fields as needed
        property_list = list(properties)  # Convert QuerySet to list for JSON serialization
        return JsonResponse({'properties': property_list})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def property_list(request):
    properties = Property.objects.all()
    user_properties = request.user.properties.all() if request.user.is_authenticated else []
    
    return render(request, 'property_list.html', {
        'properties': properties,
        'user_properties': user_properties
    })

def error(request):
    return render(request, 'error.html')


def property_reviews(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    reviews = property.ratings.all()  # Get all ratings/reviews for the property
    return render(request, 'property_reviews.html', {
        'property': property,
        'reviews': reviews
    })


@login_required
def add_rating(request, property_id):
    property_instance = get_object_or_404(Property, pk=property_id)
    
    # Check if the user has already rated this property
    existing_rating = propRating.objects.filter(property=property_instance, user=request.user).first()
    
    if request.method == "POST":
        rating_value = request.POST.get('rating')  # Get the rating from the form input
        review_text = request.POST.get('review')   # Get the review text from the form

        if existing_rating:
            # Update existing rating
            existing_rating.rating = rating_value
            existing_rating.review = review_text
            existing_rating.save()
        else:
            # Create a new rating
            propRating.objects.create(
                property=property_instance,
                user=request.user,
                rating=rating_value,
                review=review_text
            )

        # Redirect to the property detail page or home after rating is added/updated
        return redirect('main:property_detail', property_id=property_instance.id)

    # If the method is GET, render the rating form
    return render(request, 'add_rating.html', {
        'property': property_instance,
        'existing_rating': existing_rating
    })

def all_user_profiles_json(request):
    # Get all UserProfile objects
    user_profiles = UserProfile.objects.all()

    # Create a list of dictionaries to store each user profile's data
    data = []
    for user_profile in user_profiles:
        data.append({
            'username': user_profile.user.username,
            'role': user_profile.role,
        })
    
    # Return the data as JSON
    return JsonResponse(data, safe=False)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import PropertySerializer
from django.views.decorators.csrf import csrf_exempt

import logging

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.host = request.user
            property_instance.save()
            return JsonResponse({'status': 'success', 'message': 'Property added successfully'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_property(request, property_id):
    if request.method == 'POST':
        try:
            property_obj = Property.objects.get(id=property_id)
            property_obj.delete()
            return JsonResponse({'message': 'Property deleted successfully!'}, status=200)
        except Property.DoesNotExist:
            return JsonResponse({'error': 'Property not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


class PropertyListView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return properties associated with the logged-in user
        return Property.objects.filter(host=self.request.user)

    def get(self, request):
        # Fetch the properties using the overridden `get_queryset`
        properties = self.get_queryset()
        serializer = self.get_serializer(properties, many=True)
        return Response(serializer.data)    
    
    def perform_create(self, serializer):
        # Set the host to the logged-in user
        serializer.save(host=self.request.user)

@csrf_exempt
def edit_property_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            property_id = data.get('id')

            # Fetch the property instance
            property_instance = Property.objects.get(id=property_id)

            # Update the fields
            property_instance.Hotel = data.get('Hotel', property_instance.Hotel)
            property_instance.Category = data.get('Category', property_instance.Category)
            property_instance.Address = data.get('Address', property_instance.Address)
            property_instance.Contact = data.get('Contact', property_instance.Contact)
            property_instance.Price = data.get('Price', property_instance.Price)
            property_instance.Amenities = data.get('Amenities', property_instance.Amenities)
            property_instance.Image_URL = data.get('Image_URL', property_instance.Image_URL)
            property_instance.Location = data.get('Location', property_instance.Location)
            property_instance.Page_URL = data.get('Page_URL', property_instance.Page_URL)

            # Save the updated property instance
            property_instance.save()

            return JsonResponse({'status': 'success', 'message': 'Property updated successfully'})
        except Property.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Property not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    


@csrf_exempt
def get_property_details(request, property_id):
    try:
        property_instance = Property.objects.get(id=property_id)
        property_data = {
            'id': property_instance.id,
            'Hotel': property_instance.Hotel,
            'Category': property_instance.Category,
            'Address': property_instance.Address,
            'Contact': property_instance.Contact,
            'Price': property_instance.Price,
            'Amenities': property_instance.Amenities,
            'Image_URL': property_instance.Image_URL,
            'Location': property_instance.Location,
            'Page_URL': property_instance.Page_URL,
        }
        return JsonResponse(property_data, safe=False)
    except Property.DoesNotExist:
        return JsonResponse({'error': 'Property not found'}, status=404)
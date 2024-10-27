import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import PropertyForm
from .models import Property, UserProfile ,Rating, Booking
from functools import wraps

def is_host(user):
    return user.is_authenticated and user.userprofile.role == 'host'

def is_guest(user):
    return user.is_authenticated and user.userprofile.role == 'guest'

def user_is_host(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not is_host(request.user):
            return render(request, 'not_host.html')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@user_is_host
def host_dashboard(request):
    properties = request.user.properties.all() 
    bookings = Booking.objects.filter(property__in=properties)
    return render(request, 'host_dashboard.html', {'properties': properties, 'bookings': bookings})

def home(request):
    if not request.user.is_authenticated:
        return redirect('main:login')
    properties = Property.objects.order_by('?')[:6]
    user_properties = request.user.properties.all() if request.user.userprofile.role == 'host' else []
    return render(request, 'home.html', {
        'properties': properties,
        'user_properties': user_properties,
        'last_login': request.COOKIES.get('last_login')
    })

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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            role = request.POST.get('role')
            UserProfile.objects.create(user=user, role=role)

            messages.success(request, "Registration successful. You can now log in.")
            return redirect('main:login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout(request):
    auth_logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def property_detail(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    
    user_rating = None
    if request.user.is_authenticated:
        user_rating = Rating.objects.filter(property=property_instance, user=request.user).first()

    return render(request, 'property_detail.html', {
        'property': property_instance,
        'user_rating': user_rating  
    })

@user_is_host
def add_property(request):
    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES)  # Make sure to include request.FILES for file uploads
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.host = request.user  # Set the host to the logged-in user
            property_instance.save()  # Save the property instance to the database
            
            return JsonResponse({'success': True, 'message': 'Property added successfully.'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  # Return form errors in JSON format

    # Handle GET request by rendering the form
    form = PropertyForm()  # Create a blank form instance
    return render(request, 'addproperty.html', {'form': form})  # Render the form template

@user_is_host
def edit_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id, host=request.user)

    if request.method == "POST":
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully.")
            return redirect('main:my_properties')
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, 'editproperty.html', {'form': form})

@user_is_host
def delete_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.delete()
    return HttpResponseRedirect(reverse('main:host_dashboard'))

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
    existing_rating = Rating.objects.filter(property=property_instance, user=request.user).first()
    
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
            Rating.objects.create(
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

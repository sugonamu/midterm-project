from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.contrib.auth import logout as auth_logout
from main.models import UserProfile, Property
from django.core.exceptions import ValidationError

@csrf_exempt
def logout(request):
    username = request.user.username

    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
        "status": False,
        "message": "Logout failed."
        }, status=401)
    
@csrf_exempt
def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']
        role = data.get('role')

        # Check if passwords match
        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)

        # Create the new user
        user = User.objects.create_user(username=username, password=password1)

        # Assign the role
        if role in ['guest', 'host']:
            UserProfile.objects.create(user=user, role=role)
        else:
            return JsonResponse({
                "status": False,
                "message": "Invalid role."
            }, status=400)

        return JsonResponse({
            "username": user.username,
            "status": 'success',
            "message": "User created successfully!"
        }, status=200)

    # Handle the case where the method is not POST
    return JsonResponse({
        "status": False,
        "message": "Method not allowed. Please use POST."
    }, status=405)

@csrf_exempt
def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            try:
                user_profile = UserProfile.objects.get(user=user)
                role = user_profile.role
            except UserProfile.DoesNotExist:
                role = ''
            return JsonResponse({
                "username": user.username,
                "status": True,
                "role": role,
                "message": "Login successful!"
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login failed, account disabled."
            }, status=401)

    else:
        return JsonResponse({
            "status": False,
            "message": "Login failed, check email or password again."
        }, status=401)
    
from django.forms.models import model_to_dict
from main.forms import PropertyForm

@csrf_exempt 
def edit_property(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id, host=request.user)

    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON from request body
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

        # Populate the form with the received data
        form = PropertyForm(data, instance=property_instance)
        if form.is_valid():
            form.save()
            # Send success response with updated property details
            return JsonResponse({
                'message': 'Property updated successfully',
                'property': model_to_dict(property_instance),  # Convert model to dict for JSON response
            }, status=200)
        else:
            # Send validation errors back to the client
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        # For non-POST requests (like GET), return the property data
        property_data = model_to_dict(property_instance)
        return JsonResponse({'property': property_data}, status=200)


from django.http import JsonResponse

def delete_property(request, property_id):
    if request.method == 'POST':
        try:
            property_obj = Property.objects.get(id=property_id)
            property_obj.delete()
            return JsonResponse({'message': 'Property deleted successfully!'}, status=200)
        except Property.DoesNotExist:
            return JsonResponse({'error': 'Property not found'}, status=404)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF for API requests
def add_property_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Only POST requests are allowed.'}, status=405)
    
    try:
        # Parse JSON body
        data = json.loads(request.body.decode('utf-8'))

        # Extract fields from JSON
        hotel_name = data.get("hotelName")
        category = data.get("category")
        address = data.get("address")
        contact = data.get("contact")
        price = data.get("price")
        amenities = data.get("amenities")
        image_url = data.get("imageUrl")
        location = data.get("location")
        page_url = data.get("pageUrl")

        # Validate required fields
        required_fields = [hotel_name, category, address, contact, price, location]
        if any(field is None or field.strip() == '' for field in required_fields):
            return JsonResponse({'success': False, 'message': 'All fields are required.'}, status=400)

        # Create a new Property instance
        property_instance = Property(
            host=request.user,  # Assuming the user is authenticated
            hotelName=hotel_name,
            category=category,
            address=address,
            contact=contact,
            price=price,
            amenities=amenities,
            imageUrl=image_url,
            location=location,
            pageUrl=page_url
        )

        # Save the property instance
        property_instance.full_clean()  # Validate model data before saving
        property_instance.save()

        return JsonResponse({'success': True, 'message': 'Property added successfully.'}, status=201)

    except ValidationError as ve:
        # Handle validation errors
        return JsonResponse({'success': False, 'message': str(ve)}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        # Catch other exceptions and return a generic error message
        return JsonResponse({'success': False, 'message': f'An error occurred: {str(e)}'}, status=500)



from django.shortcuts import render
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import UserUpdateForm, ProfileUpdateForm  
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from .models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProfileSerializer, UserSerializer
from rest_framework import generics
from django.contrib.auth.models import User

@csrf_exempt
@login_required
def update_profile_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Get the user's profile
            profile = Profile.objects.get(user=request.user)

            # Create forms with data
            u_form = UserUpdateForm(data, instance=request.user)
            p_form = ProfileUpdateForm(data, request.FILES, instance=profile)

            # Validate and save forms
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                return JsonResponse({"status": "success", "message": "Profile updated successfully!"}, status=200)
            else:
                # Collect errors from both forms
                errors = {
                    "user_form_errors": u_form.errors,
                    "profile_form_errors": p_form.errors,
                }
                return JsonResponse({"status": "error", "errors": errors}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    elif request.method == 'GET':
        # Fetch user and profile data
        profile = Profile.objects.get(user=request.user)
        data = {
            "username": request.user.username,
            "email": request.user.email,
            "profile_picture": profile.profile_picture.url if profile.profile_picture else None,
        }
        return JsonResponse({"status": "success", "data": data}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
    
def show_json(request):
    data = Profile.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@login_required  # Ensure that only logged-in users can access this view
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    form_has_errors = False  # Initialize flag for form errors

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')  # Redirect after successful update
        else:
            messages.error(request, 'Please correct the error below.')
            form_has_errors = True  # Set flag to True if there are errors

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'profile': profile,
        'u_form': u_form,
        'p_form': p_form,
        'form_has_errors': form_has_errors,  # Pass the error flag to the context
    }
    return render(request, 'profile.html', context)


class ProfileListView(APIView):
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
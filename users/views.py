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
        profile = Profile.objects.get(user=request.user)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if u_form.is_valid():
            u_form.save()
            image_path = request.POST.get('image')
            if image_path:
                profile.image = image_path
                profile.save()
            return JsonResponse({'status': 'success', 'message': 'Profile updated successfully'}, status=200)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
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

def check_username_availability(request):
    username = request.GET.get('username', None)
    if username:
        is_available = not User.objects.filter(username=username).exists()
        return JsonResponse({'available': is_available})
    else:
        return JsonResponse({'available': False, 'error': 'Username not provided'})

class UserProfileView(APIView):
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=404)
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

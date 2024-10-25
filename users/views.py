from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import UserUpdateForm, ProfileUpdateForm  # Fixed form name typo
from django.contrib import messages

def auto_login_view(request):
    # Replace 'username' and 'password' with actual test user credentials
    username = 'test1'
    password = 'kamuaku40'
    
    try:
        # Get the user object
        user = User.objects.get(username=username)

        # Log the user in
        login(request, user)
        
        # Redirect to the profile view or any other view you want
        return redirect('profile')
    except User.DoesNotExist:
        messages.error(request, 'Test user does not exist.')
        return redirect('login')  # Redirect to the login page or wherever appropriate

@login_required  # Ensure that only logged-in users can access this view
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
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

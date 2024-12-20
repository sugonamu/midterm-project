from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get the current user
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        # Check if the username is already taken by another user
        if User.objects.filter(username=username).exists():
            # Check if the current user is not the same as the user trying to update
            if self.instance and self.instance.username != username:
                raise forms.ValidationError('This username is already taken. Please choose a different one.')

        return username


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
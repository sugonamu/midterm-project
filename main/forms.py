from django import forms
from .models import Property

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'input-class'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'input-class'})
    )
    
from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'Hotel',               # Hotel name
            'Category',            # Hotel category
            'Rating',              # Rating of the hotel
            'Address',             # Address of the hotel
            'Contact',             # Contact information
            'Price',               # Price in string format
            'Amenities',           # Amenities provided by the hotel
            'Image_URL',           # URL of the image
            'Location',            # Location of the hotel
            'Page_URL',            # URL to the hotel's page
        ]

        widgets = {
            'Hotel': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Hotel Name'}),
            'Category': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category'}),
            'Rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rating'}),
            'Address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'Contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Information'}),
            'Price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'Amenities': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Amenities'}),
            'Image_URL': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Image URL'}),
            'Location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'Page_URL': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Page URL'}),
        }


    def clean_price_per_night(self):
        price = self.cleaned_data.get('price_per_night')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_number_of_guests(self):
        guests = self.cleaned_data.get('number_of_guests')
        if guests <= 0:
            raise forms.ValidationError("Number of guests must be greater than zero.")
        return guests

    def clean_number_of_bedrooms(self):
        bedrooms = self.cleaned_data.get('number_of_bedrooms')
        if bedrooms < 0:
            raise forms.ValidationError("Number of bedrooms cannot be negative.")
        return bedrooms

    def clean_number_of_bathrooms(self):
        bathrooms = self.cleaned_data.get('number_of_bathrooms')
        if bathrooms < 0:
            raise forms.ValidationError("Number of bathrooms cannot be negative.")
        return bathrooms
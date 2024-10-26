from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'price_per_night',
            'address',
            'number_of_guests',
            'number_of_bedrooms',
            'number_of_bathrooms',
            'is_available'
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Property Description'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price per Night'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Guests'}),
            'number_of_bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Bedrooms'}),
            'number_of_bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Number of Bathrooms'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
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
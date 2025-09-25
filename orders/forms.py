from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'street_address', 'city', 'state', 'zip_code', 'country',
            'card_holder_name', 'card_number', 'expiry_date', 'cvv',
            'order_details', 'special_instructions'
        ]
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(123) 456-7890'}),
            'street_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123 Main St'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ZIP Code'}),
            'country': forms.TextInput(attrs={'class': 'form-control', 'value': 'United States'}),
            'card_holder_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on Card'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YYYY'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '123'}),
            'order_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe what you need printed...'}),
            'special_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special instructions?'}),
        }
    
    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number', '')
        # Remove spaces and validate length
        card_number = card_number.replace(' ', '')
        if len(card_number) < 13 or len(card_number) > 19:
            raise forms.ValidationError("Please enter a valid card number")
        return card_number
    
    def clean_expiry_date(self):
        expiry = self.cleaned_data.get('expiry_date', '')
        if not expiry or '/' not in expiry:
            raise forms.ValidationError("Please enter expiry date as MM/YYYY")
        return expiry
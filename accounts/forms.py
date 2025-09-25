from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'minlength': 8, 'placeholder': 'At least 8 characters'}),
        min_length=8,
        help_text='Use at least 8 characters.'
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'minlength': 8, 'placeholder': 'Re-enter your password'}),
        min_length=8
    )

    class Meta:
        model = UserModel
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'minlength': 3, 'maxlength': 50, 'placeholder': 'Choose a username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes and mark invalid fields
        for name, field in self.fields.items():
            base = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = (base + ' form-control').strip()
            if self.errors.get(name):
                field.widget.attrs['class'] += ' is-invalid'
                field.widget.attrs['aria-invalid'] = 'true'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and UserModel.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and UserModel.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email already exists.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        # If your custom user uses email as the username, no explicit username is required.
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

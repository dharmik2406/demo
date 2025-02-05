from django import forms
from django.contrib.auth.forms import AuthenticationForm 
from .models import User

# Registration form
from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data


# Login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter password'
    }))

# Password reset request form
class PasswordResetRequestForm(forms.Form):
      email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

# Password reset form
class PasswordResetForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs=
    {'class': 'form-control', 'placeholder': 'Enter OTP'}))
    new_password = forms.CharField(
    widget=forms.PasswordInput(attrs=
    {'class': 'form-control', 'placeholder': 'Enter New Password'})
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs=
    {'class': 'form-control', 'placeholder': 'Confirm New Password'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return cleaned_data
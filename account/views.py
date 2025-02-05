from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
from .models import OTP,product
import random


def product_list(request):
    return render()





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  
            user.save()
            login(request, user)
            return redirect('login')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# Password reset request (send OTP)
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                otp_code = str(random.randint(100000, 999999))
                otp = OTP.objects.create(user=user, otp_code=otp_code)
                send_mail(
                    'Password Reset OTP',
                    f'Your OTP code is: {otp_code}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return redirect('password_reset_verify', otp_id=otp.id)
            else:
                messages.error(request, "No user found with this email.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_request.html', {'form': form})


def password_reset_verify(request, otp_id):
    otp = get_object_or_404(OTP, id=otp_id)

    if otp.is_expired():
        messages.error(request, 'OTP has expired.')
        return redirect('password_reset_request')

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if entered_otp == otp.otp_code:
                user = otp.user
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                otp.is_verified = True
                otp.save()
                messages.success(request, 'Password reset successful. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, "Invalid OTP.")
    else:
        form = PasswordResetForm()

    return render(request, 'password_reset_verify.html', {'form': form, 'otp_id': otp.id})

# Home view
def dashboard(request):
    return render(request  , 'dashboard.html')


def firstpage(request):
    return render(request  , 'firstpage.html')


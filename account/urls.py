from django.urls import path
from . import views

urlpatterns = [
    path('', views.firstpage , name='firstpage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('password-reset-request/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-verify/<int:otp_id>/', views.password_reset_verify, name='password_reset_verify'),
    path('dashboard/', views.dashboard , name='dashboard'),

]

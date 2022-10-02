from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views as v

urlpatterns = [
    path('register/', v.register, name='register'),
    path('profile/', v.profile, name='profile'),
    path('settings/', v.settings, name='settings'),
    path('activate/<uidb64>/<token>', v.activate, name='activate'),
    path('password_reset/', v.password_reset, name='password_reset'),
    path('reset/<uidb64>/<token>', v.reset, name='reset'),   
    path('resend_confirmation/', v.resend_confirm, name='resend'),
]
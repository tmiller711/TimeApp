from django.urls import path

from . import views
# import models

urlpatterns = [
    path('', views.home, name='home')
]
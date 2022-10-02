from django.urls import path

from . import views
# import models

app_name = 'cal'
urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('<int:year>-<int:month>-<int:day>/', views.day, name='day'),
]
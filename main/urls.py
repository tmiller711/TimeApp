from django.urls import path

from . import views
# import models

app_name = 'cal'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar')
]
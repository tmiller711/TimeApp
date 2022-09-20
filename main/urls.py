from django.urls import path

from . import views
# import models

app_name = 'cal'
urlpatterns = [
    path('', views.CalendarView.as_view(), name='calendar'),
    path('<int:year>-<int:month>-<int:day>/', views.day, name='day'),
    path(r'^event/new/$', views.event, name='event_new'),
    path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]
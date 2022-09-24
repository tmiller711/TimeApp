from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=200, blank=True)
    timezone = models.CharField(max_length=50, default='America/Chicago')
    wake_up_time = models.TimeField(default=datetime.time(8, 0))
    bedtime = models.TimeField(default=datetime.time(22, 0))
    date_registered = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.user)
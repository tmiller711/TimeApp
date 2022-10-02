from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from register.models import Account

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    @property
    def get_html_url(self):
        url = reverse('cal:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'

class Block(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.topic

class Task(models.Model):
    name = models.CharField(max_length=200)
    complete = models.BooleanField(default=False)
    block = models.ForeignKey(Block, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager
import datetime

class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email = self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username=username,
            password = password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    timezone = models.CharField(max_length=50, default='America/Chicago')
    wake_up_time = models.TimeField(default=datetime.time(8, 0))
    bedtime = models.TimeField(default=datetime.time(22, 0))
    theme = models.CharField(max_length=30, default="light")

    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # this will set whatever you want to use to login with
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

# Create your models here.
# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200, blank=True)
#     phone = models.CharField(max_length=200, blank=True)
#     timezone = models.CharField(max_length=50, default='America/Chicago')
#     wake_up_time = models.TimeField(default=datetime.time(8, 0))
#     bedtime = models.TimeField(default=datetime.time(22, 0))
#     date_registered = models.DateTimeField(auto_now_add=True, null=True)

#     def __str__(self):
#         return str(self.user)
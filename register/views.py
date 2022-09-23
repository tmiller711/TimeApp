from django.shortcuts import render, redirect
from .forms import RegisterForm, UserProfileForm, UserSettingsForm
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.
def register(request):
    user = request.user
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})

def profile(request):
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=userprofile)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=userprofile)

    return render(request, "register/profile.html", {'form': form})

def settings(request):
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=userprofile)
        if form.is_valid():
            form.save()
    else:
        form = UserSettingsForm(instance=userprofile)

    return render(request, "register/settings.html", {'form': form})
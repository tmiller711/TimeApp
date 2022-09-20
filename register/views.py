from django.shortcuts import render, redirect
from .forms import RegisterForm
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
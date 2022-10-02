from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.contrib import messages

from .forms import RegisterForm, UserProfileForm, UserSettingsForm, ResendConfirmationForm, PasswordResetForm
from .models import Account
from .tokens import accounts_activation_token

def register(request):
    user = request.user
    # print(user)
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))

        return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})

def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "register/profile.html", {'form': form})

def settings(request):
    if request.method == "POST":
        form = UserSettingsForm(request.POST, instance=request.user)
        print(form['wake_up_time'])
        if form.is_valid():
            form.save()
    else:
        form = UserSettingsForm(instance=request.user)

    return render(request, "register/settings.html", {'form': form})


# password reset functionality
def password_reset(request):
    if request.method == "POST":
        form = ResendConfirmationForm(request.POST)
        if form.is_valid():
            try:
                user = Account.objects.get(email=form.cleaned_data.get('email'))
                print(user)
                send_password_reset(request, user, form.cleaned_data.get('email'))
                return redirect('/login')
            except Exception as e:
                print(e)
                messages.error(request, "Could not find an active account with that email. Do you need to <a href='/resend_confirmation'>Resend Confirmation Email</a> first?")
                return redirect('/login')
    else:
        form = ResendConfirmationForm()
    return render(request, 'register/resend_confirm.html', {'form': form})

def send_password_reset(request, user, to_email):
    mail_subject = "Reset your account password"
    message = render_to_string("template_password_reset.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': accounts_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        print("sent")
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received reset password link to confirm and complete the reset. <b>Note:</b> Check your spam folder.')
    else:
        print("not sent")
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

def reset(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and accounts_activation_token.check_token(user, token):
        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data.get('password1'))
                user.save()
                messages.success(request, "Password successfully changed!")
            else:
                print('invalid form')
            return redirect('/login')
        else:
            form = PasswordResetForm()
            return render(request, 'register/password_reset.html', {'form': form})


# email activation functionality
def resend_confirm(request):
    if request.method == "POST":
        form = ResendConfirmationForm(request.POST)
        if form.is_valid():
            try:
                user = Account.objects.get(email=form.cleaned_data.get('email'), is_active=False)
                activate_email(request, user, form.cleaned_data.get('email'))
                return redirect('/login')
            except:
                messages.error(request, "Could not find an unactivated account with that email")
                return redirect('/resend_confirmation/')
    else:
        form = ResendConfirmationForm()
    return render(request, 'register/resend_confirm.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and accounts_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        
        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        login(request, user, backend='register.backends.CaseInsensitiveModelBackend')

        return redirect('/')
    else:
        messages.error(request, "Activation link is invalid! Click here to send another <a href='/resendconfirmation'>Resend</a>")
    return redirect('/')

def activate_email(request, user, to_email):
    mail_subject = "Activate your user accounts"
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': accounts_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        print("sent")
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        print("not sent")
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')
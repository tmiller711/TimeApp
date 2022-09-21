import re

from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(url) for url in settings.LOGIN_EXEMPT_URLS]

# instead of adding the login_required decorator to each view this does it for us
class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    # this method will run right before django is going to call any view
    def process_view(self, request, view_func, view_args, view_kwargs):
        # will check if request.user exists
        assert hasattr(request, 'user')
        path = request.path_info.lstrip('/')

        # if not request.user.is_authenticated:
        #     # checks if user is trying to reach non exempt url
        #     if not any(url.match(path) for url in EXEMPT_URLS):
        #         return redirect(settings.LOGIN_URL)

        url_is_exempt = any(url.match(path) for url in EXEMPT_URLS)

        if path == 'logout/':
            logout(request)

        if request.user.is_authenticated and url_is_exempt:
            return redirect(settings.LOGIN_REDIRECT_URL)

        elif request.user.is_authenticated or url_is_exempt:
            return None

        else:
            return redirect(settings.LOGIN_URL)
from urllib.parse import quote_plus

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.urls import reverse

from doorkeeper.helpers import encode_password, get_doorkeeper_setting


class DoorkeeperMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self._should_bypass_doorkeeper(request, view_func):
            if self.is_doorkeeper_entrance_view(view_func):
                return HttpResponseRedirect(get_doorkeeper_setting("DEFAULT_REDIRECT_URL"))
            return None

        if self.is_doorkeeper_entrance_view(view_func):
            return None

        # Otherwise, redirect to the doorkeeper password prompt
        return self.generate_doorkeeper_redirect_response(request)

    def is_doorkeeper_entrance_view(self, view_func):
        return getattr(view_func, "is_doorkeeper_entrance", False)

    def _should_bypass_doorkeeper(self, request, view_func):
        # If doorkeeper is not enabled, proceed
        if not get_doorkeeper_setting("ENABLED"):
            return True

        # If the user has already had their password checked, proceed
        if self._check_doorkeeper_cookie(request):
            return True

        # If the view is exempt from doorkeeper, proceed
        if getattr(view_func, "doorkeeper_exempt", False):
            return True

        # If the path is exempt from doorkeeper, proceed
        if request.path in get_doorkeeper_setting("BYPASS_PATHS"):
            return True

        return False

    def generate_doorkeeper_redirect_response(self, request):
        return redirect_to_login(
            request.path,
            login_url=reverse("doorkeeper:entrance"),
            redirect_field_name=get_doorkeeper_setting("NEXT_URL_PARAM_NAME"),
        )

    def _check_doorkeeper_cookie(self, request):
        return request.COOKIES.get(get_doorkeeper_setting("COOKIE_NAME")) == encode_password(
            get_doorkeeper_setting("PASSWORD")
        )

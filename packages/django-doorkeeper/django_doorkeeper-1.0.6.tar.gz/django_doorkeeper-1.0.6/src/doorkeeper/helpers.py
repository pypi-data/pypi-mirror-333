from hashlib import sha256
from typing import Any

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.urls import reverse_lazy

DEFAULT_SETTINGS = {
    "BYPASS_PATHS": [],
    "COOKIE_NAME": "doorkeeper_cookie",
    "NEXT_URL_PARAM_NAME": "doorkeeper_next_url",
    "REDIRECT_ALLOWED_HOSTS": [],
    "EXIT_REDIRECT_URL": reverse_lazy("doorkeeper:entrance"),
}

DJANGO_FALLBACK_SETTINGS = {
    "COOKIE_AGE": "SESSION_COOKIE_AGE",
    "COOKIE_DOMAIN": "SESSION_COOKIE_DOMAIN",
    "COOKIE_EXPIRE_AT_BROWSER_CLOSE": "SESSION_EXPIRE_AT_BROWSER_CLOSE",
    "COOKIE_HTTPONLY": "SESSION_COOKIE_HTTPONLY",
    "COOKIE_PATH": "SESSION_COOKIE_PATH",
    "COOKIE_SAMESITE": "SESSION_COOKIE_SAMESITE",
    "COOKIE_SECURE": "SESSION_COOKIE_SECURE",
}

REQUIRED_SETTINGS = {
    "PASSWORD",
    "ENABLED",
    "DEFAULT_REDIRECT_URL",
}


def get_doorkeeper_setting(key: str, default: Any = None) -> Any:
    if not hasattr(django_settings, "DOORKEEPER"):
        raise ImproperlyConfigured("DOORKEEPER is not configured in Django settings")

    doorkeeper_settings = django_settings.DOORKEEPER

    if key not in doorkeeper_settings:

        if key in REQUIRED_SETTINGS:
            raise ImproperlyConfigured(f"{key} must be set in DOORKEEPER settings")

        if key in DJANGO_FALLBACK_SETTINGS:
            return getattr(django_settings, DJANGO_FALLBACK_SETTINGS[key], default)

        if key in DEFAULT_SETTINGS:
            return DEFAULT_SETTINGS[key]

        return default

    return doorkeeper_settings[key]


def encode_password(password: str) -> str:
    return sha256(f"{password}::{django_settings.SECRET_KEY}".encode()).hexdigest()


def set_doorkeeper_cookie(response: HttpResponse, password: str) -> None:
    response.set_cookie(
        get_doorkeeper_setting("COOKIE_NAME"),
        encode_password(get_doorkeeper_setting("PASSWORD")),
        max_age=get_doorkeeper_setting("COOKIE_AGE"),
        expires=get_doorkeeper_setting("COOKIE_EXPIRE_AT_BROWSER_CLOSE"),
        domain=get_doorkeeper_setting("COOKIE_DOMAIN"),
        path=get_doorkeeper_setting("COOKIE_PATH"),
        secure=get_doorkeeper_setting("COOKIE_SECURE") or None,
        httponly=get_doorkeeper_setting("COOKIE_HTTPONLY") or None,
        samesite=get_doorkeeper_setting("COOKIE_SAMESITE"),
    )


def delete_doorkeeper_cookie(response: HttpResponse) -> None:
    response.delete_cookie(
        get_doorkeeper_setting("COOKIE_NAME"),
        path=get_doorkeeper_setting("COOKIE_PATH"),
        domain=get_doorkeeper_setting("COOKIE_DOMAIN"),
    )

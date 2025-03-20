from django.http import HttpResponse


def protected_view(request):
    """A view that should be protected by doorkeeper."""
    return HttpResponse("Protected content")


def public_view(request):
    """A view that should be accessible without authentication."""
    return HttpResponse("Public content")


def exempt_view(request):
    """A view that should be exempt from doorkeeper protection."""
    return HttpResponse("Exempt content")

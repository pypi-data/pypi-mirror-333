from hashlib import md5

from django.http import HttpResponseRedirect
from django.utils.encoding import iri_to_uri
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView

from doorkeeper.forms import DoorkeeperEntranceForm
from doorkeeper.helpers import (
    delete_doorkeeper_cookie,
    get_doorkeeper_setting,
    set_doorkeeper_cookie,
)


class DoorkeeperEntranceView(FormView):
    http_method_names = ["get", "post"]
    template_name = "doorkeeper/doorkeeper_entrance.html"
    form_class = DoorkeeperEntranceForm

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.redirect_allowed_hosts = get_doorkeeper_setting("REDIRECT_ALLOWED_HOSTS", [])

    def dispatch(self, request, *args, **kwargs):
        self.next_url_param_name = get_doorkeeper_setting("NEXT_URL_PARAM_NAME")
        self.next_url = request.GET.get(self.next_url_param_name) or request.POST.get(self.next_url_param_name)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        set_doorkeeper_cookie(response, get_doorkeeper_setting("PASSWORD"))
        return response

    def get_success_url(self):
        if self.next_url and url_has_allowed_host_and_scheme(
            self.next_url,
            allowed_hosts=[self.request.get_host(), *self.redirect_allowed_hosts],
            require_https=self.request.is_secure(),
        ):
            return iri_to_uri(self.next_url)

        return get_doorkeeper_setting("DEFAULT_REDIRECT_URL")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["next_url"] = self.next_url
        context["next_url_param_name"] = self.next_url_param_name
        return context


class DoorkeeperExitView(RedirectView):
    http_method_names = ["post"]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = get_doorkeeper_setting("EXIT_REDIRECT_URL")

    def post(self, request, *args, **kwargs):
        url = self.get_redirect_url(*args, **kwargs)
        response = HttpResponseRedirect(url)
        delete_doorkeeper_cookie(response)
        return response

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args, **kwargs)

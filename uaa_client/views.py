from urllib.parse import urlencode

import django.contrib.auth
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, render
from django.utils.crypto import get_random_string
from django.utils.http import is_safe_url

from .compat import reverse
from .authentication import get_auth_url


def login_error(request, error_code):
    return render(request, "uaa_client/login_error.html", {"error_code": error_code})


def login(request):
    redirect_uri = request.build_absolute_uri(reverse("uaa_client:callback"))
    request.session["oauth2_next_url"] = request.GET.get("next", "")
    request.session["oauth2_state"] = get_random_string(length=32)
    url = (
        get_auth_url(request)
        + "?"
        + urlencode(
            {
                "client_id": settings.UAA_CLIENT_ID,
                "response_type": "code",
                "redirect_uri": redirect_uri,
                "state": request.session["oauth2_state"],
            }
        )
    )

    return HttpResponseRedirect(url)


def oauth2_callback(request):
    code = request.GET.get("code")
    expected_state = request.session.get("oauth2_state")
    state = request.GET.get("state")

    if state is None:
        return login_error(request, "missing_state")

    if expected_state is None:
        return login_error(request, "missing_session_state")

    if state != expected_state:
        return login_error(request, "invalid_state")

    if code is None:
        return login_error(request, "missing_code")

    user = django.contrib.auth.authenticate(request, uaa_oauth2_code=code)

    if user is None:
        return login_error(request, "authenticate_failed")

    del request.session["oauth2_state"]

    django.contrib.auth.login(request, user)

    next_url = request.session["oauth2_next_url"]
    del request.session["oauth2_next_url"]

    if not is_safe_url(url=next_url, allowed_hosts=[request.get_host()]):
        next_url = resolve_url(request.build_absolute_uri(settings.LOGIN_REDIRECT_URL))

    return HttpResponseRedirect(next_url)

from urllib.parse import urlencode
from datetime import timedelta
import json
import jwt
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect

from .compat import reverse
from .middleware import uaa_refresh_exempt


TOKEN_EXPIRATION = timedelta(seconds=60)


def expect(a, b):
    if a != b:
        print("Warning: Expected %s to equal %s." % (a, b))  # pragma: no cover


@require_GET
def authorize(request):
    expect(request.GET.get("client_id"), settings.UAA_CLIENT_ID)
    expect(request.GET.get("response_type"), "code")

    email = request.GET.get("email")

    if not email:
        return render(
            request, "uaa_client/fake_uaa_provider/index.html", {"query": request.GET}
        )

    url = request.build_absolute_uri(reverse("uaa_client:callback"))

    qs = urlencode({"state": request.GET.get("state", ""), "code": email})
    return HttpResponseRedirect("%s?%s" % (url, qs))


@uaa_refresh_exempt
@csrf_exempt
@require_POST
def access_token(request):
    client_id = settings.UAA_CLIENT_ID

    grant_type = request.POST.get("grant_type")

    if grant_type == "authorization_code":
        email = request.POST["code"]
        expect(request.POST.get("response_type"), "token")
    elif grant_type == "refresh_token":
        preamble, email = request.POST["refresh_token"].split(":")
        expect(preamble, "fake_oauth2_refresh_token")
    else:
        return HttpResponseBadRequest("Invalid grant_type: %s" % grant_type)

    expect(request.POST.get("client_id"), client_id)
    expect(request.POST.get("client_secret"), settings.UAA_CLIENT_SECRET)

    res = HttpResponse()
    res["content-type"] = "application/json"
    access_token_contents = {
        "aud": ["openid", client_id],
        "auth_time": 1466765095,
        "azp": client_id,
        "cid": client_id,
        "client_id": client_id,
        "email": email,
        # This is the "Expiration Time" claim of the JWT:
        # https://tools.ietf.org/html/rfc7519#section-4.1.4
        "exp": 1466808304,
        "grant_type": "authorization_code",
        # This is the "Issued At" claim of the JWT:
        # https://tools.ietf.org/html/rfc7519#section-4.1.6
        "iat": 1466765104,
        "iss": "https://uaa.cloud.gov/oauth/token",
        "jti": "fake_jti",
        "origin": "gsa.gov",
        "rev_sig": "9ad72122",
        "scope": ["openid"],
        "sub": "12345678-1234-1234-1234-123456789abc",
        "user_id": "12345678-1234-1234-1234-123456789abc",
        "user_name": email,
        "zid": "uaa",
    }

    # The client won't need to verify this because it will be communicating
    # directly with the ID provider (i.e., us) over an intermediary-free
    # trusted channel, using its client secret to authenticate with us.
    #
    # https://developers.google.com/identity/protocols/OpenIDConnect#obtainuserinfo
    access_token = jwt.encode(
        access_token_contents, "unused secret key (for verification)"
    )

    res.content = json.dumps(
        {
            "access_token": access_token.decode("ascii"),
            "expires_in": int(TOKEN_EXPIRATION.total_seconds()),
            "jti": "fake_jti",
            "refresh_token": "fake_oauth2_refresh_token:%s" % email,
            "scope": "openid",
            "token_type": "bearer",
        }
    )

    return res

from unittest import mock
import json
import urllib.parse
from typing import Dict, Any  # NOQA
import jwt
from django.test import TestCase, RequestFactory
from django.test.utils import override_settings
from django.contrib.auth.models import User
import httmock

from .. import authentication as auth


get_user_by_email = auth.UaaBackend.get_user_by_email


@override_settings(
    DEBUG=True,
    UAA_CLIENT_ID="clientid",
    UAA_CLIENT_SECRET="clientsecret",
    UAA_AUTH_URL="fake:",
    UAA_TOKEN_URL="fake:",
)
class FakeAuthenticationTests(TestCase):
    AUTH_PATH = "/auth/fake/oauth/authorize"
    TOKEN_PATH = "/auth/fake/oauth/token"

    def test_get_auth_url_works(self):
        req = RequestFactory().get("/")
        self.assertEqual(auth.get_auth_url(req), "http://testserver" + self.AUTH_PATH)

    def test_get_token_url_works(self):
        req = RequestFactory().get("/")
        self.assertEqual(auth.get_token_url(req), "http://testserver" + self.TOKEN_PATH)

    def test_authorize_endpoint_displays_page_without_email(self):
        res = self.client.get(
            self.AUTH_PATH, {"client_id": "clientid", "response_type": "code"}
        )
        self.assertEqual(res.status_code, 200)

    def test_authorize_endpoint_redirects_with_email(self):
        res = self.client.get(
            self.AUTH_PATH,
            {"client_id": "clientid", "response_type": "code", "email": "boop@gsa.gov"},
        )
        self.assertEqual(res.status_code, 302)

    def test_token_endpoint_returns_400_on_invalid_grant_type(self):
        res = self.client.post(self.TOKEN_PATH, {"grant_type": "zzz"})
        self.assertEqual(res.status_code, 400)

    def test_token_endpoint_supports_refresh(self):
        res = self.client.post(
            self.TOKEN_PATH,
            {
                "client_id": "clientid",
                "client_secret": "clientsecret",
                "grant_type": "refresh_token",
                "refresh_token": "fake_oauth2_refresh_token:bap@gsa.gov",
            },
        )
        self.assertEqual(res.status_code, 200)
        obj = json.loads(res.content.decode("utf-8"))
        user_info = jwt.decode(obj["access_token"], verify=False)
        self.assertEqual(user_info["email"], "bap@gsa.gov")

    def test_token_endpoint_works(self):
        res = self.client.post(
            self.TOKEN_PATH,
            {
                "client_id": "clientid",
                "client_secret": "clientsecret",
                "grant_type": "authorization_code",
                "response_type": "token",
                "code": "boop@gsa.gov",
            },
        )
        self.assertEqual(res.status_code, 200)
        obj = json.loads(res.content.decode("utf-8"))
        user_info = jwt.decode(obj["access_token"], verify=False)
        self.assertEqual(user_info["email"], "boop@gsa.gov")

    @override_settings(DEBUG=False)
    def test_authorize_endpoint_404s_when_debug_is_false(self):
        res = self.client.get(self.AUTH_PATH)
        self.assertEqual(res.status_code, 404)

    @override_settings(DEBUG=False)
    def test_token_endpoint_404s_when_debug_is_false(self):
        res = self.client.post(self.TOKEN_PATH)
        self.assertEqual(res.status_code, 404)


@override_settings(
    UAA_CLIENT_ID="clientid",
    UAA_CLIENT_SECRET="clientsecret",
    UAA_AUTH_URL="https://example.org/auth",
    UAA_TOKEN_URL="https://example.org/token",
)
class AuthenticationTests(TestCase):
    def test_get_auth_url_works(self):
        self.assertEqual(auth.get_auth_url(None), "https://example.org/auth")

    def test_get_token_url_works(self):
        self.assertEqual(auth.get_token_url(None), "https://example.org/token")

    @mock.patch("uaa_client.authentication.logger.warning")
    def test_update_access_token_returns_none_on_failure(self, m):
        def mock_404_response(url, request):
            return httmock.response(404, "nope")

        req = mock.MagicMock()
        with httmock.HTTMock(mock_404_response):
            self.assertEqual(auth.update_access_token_with_refresh_token(req), None)
        m.assert_called_with(
            "POST https://example.org/token returned 404 " "w/ content b'nope'"
        )

    @mock.patch("time.time", return_value=100)
    def test_update_access_token_returns_token_on_success(self, mock_time):
        def mock_200_response(url, request):
            self.assertEqual(request.url, "https://example.org/token")
            body = dict(urllib.parse.parse_qsl(request.body))
            self.assertEqual(
                body,
                {
                    "client_id": "clientid",
                    "client_secret": "clientsecret",
                    "grant_type": "refresh_token",
                    "refresh_token": "boop",
                },
            )
            return httmock.response(
                200,
                {"access_token": "lol", "refresh_token": "blap", "expires_in": 10},
                {"content-type": "application/json"},
            )

        req = mock.MagicMock()
        req.build_absolute_uri.return_value = "https://redirect_uri"
        session = {"uaa_refresh_token": "boop"}
        req.session.__getitem__.side_effect = session.__getitem__
        req.session.__setitem__.side_effect = session.__setitem__

        with httmock.HTTMock(mock_200_response):
            self.assertEqual(auth.update_access_token_with_refresh_token(req), "lol")

        self.assertEqual(session, {"uaa_expiry": 110, "uaa_refresh_token": "blap"})

    @mock.patch("uaa_client.authentication.logger.warning")
    def test_exchange_code_for_access_token_returns_none_on_failure(self, m):
        def mock_404_response(url, request):
            return httmock.response(404, "nope")

        req = mock.MagicMock()
        with httmock.HTTMock(mock_404_response):
            self.assertEqual(auth.exchange_code_for_access_token(req, "u"), None)
        m.assert_called_with(
            "POST https://example.org/token returned 404 " "w/ content b'nope'"
        )

    @mock.patch("time.time", return_value=100)
    def test_exchange_code_for_access_token_returns_token_on_success(self, mock_time):
        def mock_200_response(url, request):
            self.assertEqual(request.url, "https://example.org/token")
            body = dict(urllib.parse.parse_qsl(request.body))
            self.assertEqual(
                body,
                {
                    "code": "foo",
                    "client_id": "clientid",
                    "client_secret": "clientsecret",
                    "grant_type": "authorization_code",
                    "redirect_uri": "https://redirect_uri",
                    "response_type": "token",
                },
            )
            return httmock.response(
                200,
                {"access_token": "lol", "refresh_token": "boop", "expires_in": 15},
                {"content-type": "application/json"},
            )

        req = mock.MagicMock()
        req.build_absolute_uri.return_value = "https://redirect_uri"
        session = {}  # type: Dict[str, Any]
        req.session.__setitem__.side_effect = session.__setitem__

        with httmock.HTTMock(mock_200_response):
            self.assertEqual(auth.exchange_code_for_access_token(req, "foo"), "lol")

        self.assertEqual(session, {"uaa_expiry": 115, "uaa_refresh_token": "boop"})

    def test_get_user_by_email_returns_existing_user(self):
        user = User.objects.create_user("foo", "foo@example.org")
        self.assertEqual(get_user_by_email("foo@example.org"), user)

    def test_get_user_by_email_is_case_insensitive(self):
        user = User.objects.create_user("foo", "FOO@example.org")
        self.assertEqual(get_user_by_email("foo@example.org"), user)
        user = User.objects.create_user("bar", "bar@example.org")
        self.assertEqual(get_user_by_email("BAR@example.org"), user)

    @mock.patch("uaa_client.authentication.logger.info")
    def test_get_user_by_email_returns_none_when_user_does_not_exist(self, m):
        self.assertEqual(get_user_by_email("foo@example.org"), None)
        m.assert_called_with(
            "User with email foo@example.org does not exist"
            " and is not approved for auto-creation"
        )

    @mock.patch("uaa_client.authentication.logger.warning")
    def test_get_user_by_email_returns_none_when_many_users_exist(self, m):
        User.objects.create_user("foo1", "foo@example.org")
        User.objects.create_user("foo2", "foo@example.org")
        self.assertEqual(get_user_by_email("foo@example.org"), None)
        m.assert_called_with("Multiple users with email foo@example.org exist")

    def test_authenticate_returns_none_when_kwargs_not_passed(self):
        req = RequestFactory().get("/")
        backend = auth.UaaBackend()
        self.assertEqual(backend.authenticate(req), None)

    @mock.patch(
        "uaa_client.authentication.exchange_code_for_access_token", return_value=None
    )
    def test_authenticate_returns_none_when_code_is_invalid(self, m):
        req = RequestFactory().get("/")
        backend = auth.UaaBackend()
        self.assertEqual(backend.authenticate(req, "invalidcode"), None)
        m.assert_called_with(req, "invalidcode")

    def test_authenticate_returns_user_on_success(self):
        req = RequestFactory().get("/")
        backend = auth.UaaBackend()
        access_token = jwt.encode(
            {"email": "foo@example.org"}, "unused secret key"
        ).decode("ascii")
        User.objects.create_user("foo", "foo@example.org")

        with mock.patch(
            "uaa_client.authentication.exchange_code_for_access_token",
            return_value=access_token,
        ) as ex:
            user = backend.authenticate(req, "validcode")
            self.assertEqual(user.email, "foo@example.org")
            ex.assert_called_with(req, "validcode")

    def test_get_user_returns_none_when_id_is_invalid(self):
        backend = auth.UaaBackend()
        self.assertEqual(backend.get_user(32434), None)

    def test_get_user_returns_user_when_id_is_valid(self):
        backend = auth.UaaBackend()
        user = User.objects.create_user("foo", "foo@example.org")
        self.assertEqual(backend.get_user(user.id), user)

    @override_settings(UAA_APPROVED_DOMAINS=["example.org"])
    @mock.patch(
        "uaa_client.authentication.exchange_code_for_access_token",
        return_value="anything",
    )
    @mock.patch("jwt.decode", return_value={"email": "foo@example.org"})
    def test_create_user_when_domain_is_approved(self, m1, m2):
        backend = auth.UaaBackend()
        user = backend.authenticate("validcode", "req")
        self.assertEqual(user.email, "foo@example.org")

    @override_settings(UAA_APPROVED_DOMAINS=["example.org"])
    @mock.patch(
        "uaa_client.authentication.exchange_code_for_access_token",
        return_value="anything",
    )
    @mock.patch("jwt.decode", return_value={"email": "foo.person@example.org"})
    def test_slugify_user_when_domain_is_approved(self, m1, m2):
        backend = auth.UaaBackend()
        user = backend.authenticate("validcode", "req")
        self.assertEqual(user.username, "foo.person@example.org")

    @override_settings(UAA_APPROVED_DOMAINS=["example.org"])
    @mock.patch(
        "uaa_client.authentication.exchange_code_for_access_token",
        return_value="anything",
    )
    @mock.patch("jwt.decode", return_value={"email": "foo@thewrongplace.org"})
    def test_do_not_create_user_when_domain_is_not_approved(self, m1, m2):
        backend = auth.UaaBackend()
        user = backend.authenticate("validcode", "req")
        self.assertEqual(user, None)

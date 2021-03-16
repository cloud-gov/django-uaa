from unittest import mock
import urllib.parse
from django.test import TestCase
from django.test.utils import override_settings
from contextlib import contextmanager


def get_query(urlinfo):
    return dict(urllib.parse.parse_qsl(urlinfo.query))


@override_settings(
    UAA_CLIENT_ID="clientid",
    UAA_CLIENT_SECRET="clientsecret",
    UAA_AUTH_URL="https://example.org/auth",
    UAA_TOKEN_URL="https://example.org/token",
    LOGIN_REDIRECT_URL="/boop",
)
class ViewTests(TestCase):
    def assertErrorCode(self, response, error_code):
        self.assertEqual(response.context["error_code"], error_code)

    def set_session_kvs(self, **kvs):
        # session must be stored as a local variable to make modifications
        # because a new SessionStore is created every time that key
        # is accessed
        # https://docs.djangoproject.com/en/1.9/topics/testing/tools/#django.test.Client.session
        session = self.client.session
        session.update(kvs)
        session.save()

    @mock.patch("uaa_client.views.get_random_string", return_value="abcd")
    def test_login_redirects_to_uaa(self, get_random_string):
        response = self.client.get("/auth/login")
        self.assertEqual(response.status_code, 302)
        urlinfo = urllib.parse.urlparse(response["location"])
        self.assertEqual(urlinfo.scheme, "https")
        self.assertEqual(urlinfo.netloc, "example.org")
        self.assertEqual(urlinfo.path, "/auth")
        self.assertEqual(
            get_query(urlinfo),
            {
                "client_id": "clientid",
                "response_type": "code",
                "state": "abcd",
                "redirect_uri": "http://testserver/auth/callback",
            },
        )
        get_random_string.assert_called_with(length=32)

    @mock.patch("uaa_client.views.get_random_string", return_value="abcd")
    def test_login_stores_oauth2_state(self, _):
        self.client.get("/auth/login")
        self.assertEqual(self.client.session["oauth2_state"], "abcd")

    def test_callback_reports_missing_state_in_querystring(self):
        response = self.client.get("/auth/callback")
        self.assertErrorCode(response, "missing_state")

    def test_callback_reports_missing_state_in_session(self):
        response = self.client.get("/auth/callback?state=acbd")
        self.assertErrorCode(response, "missing_session_state")

    def test_callback_reports_mismatched_state(self):
        self.set_session_kvs(oauth2_state="different")
        response = self.client.get("/auth/callback?state=abcd")
        self.assertErrorCode(response, "invalid_state")

    def test_callback_reports_missing_code_in_querystring(self):
        self.set_session_kvs(oauth2_state="abcd")
        response = self.client.get("/auth/callback?state=abcd")
        self.assertErrorCode(response, "missing_code")

    @mock.patch("django.contrib.auth.authenticate", return_value=None)
    def test_callback_reports_authenticate_failed(self, _):
        self.set_session_kvs(oauth2_state="abcd")
        response = self.client.get("/auth/callback?state=abcd&code=code")
        self.assertErrorCode(response, "authenticate_failed")

    @contextmanager
    def login_via_callback(self, user="u", next_url=""):
        self.set_session_kvs(oauth2_state="a", oauth2_next_url=next_url)
        with mock.patch("django.contrib.auth.login") as login_mock:
            with mock.patch("django.contrib.auth.authenticate", return_value=user):
                response = self.client.get("/auth/callback?state=a&code=c")
                self.assertEqual(login_mock.call_args[0][1], "u")
                yield response

    def test_callback_redirects_to_next(self):
        with self.login_via_callback(next_url="/admin") as response:
            self.assertEqual(response.status_code, 302)
            urlinfo = urllib.parse.urlparse(response["location"])
            self.assertEqual(urlinfo.path, "/admin")

    def test_callback_redirects_to_login_url_on_unsafe_next(self):
        with self.login_via_callback(next_url="http://evil.com") as response:
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response["location"], "http://testserver/boop")

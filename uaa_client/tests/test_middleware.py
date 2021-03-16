from unittest.mock import patch
from django.test import TestCase

from .. import middleware
from ..middleware import UaaRefreshMiddleware, uaa_refresh_exempt


def noop():
    pass


class FakeUser:
    def __init__(self, is_authenticated):
        self.username = "foo"
        self._is_authenticated = is_authenticated

    def is_authenticated(self):
        return self._is_authenticated


class FakeRequest:
    def __init__(self, is_authenticated=True, session=None):
        self.user = FakeUser(is_authenticated)
        self.session = session or {}


class MiddlewareTests(TestCase):
    def assertNoRefresh(self, request, view_func=noop, time=0):
        mw = UaaRefreshMiddleware()

        with patch("time.time", return_value=time):
            with patch.object(mw, "_refresh") as m:
                mw.process_view(request, view_func, [], {})
                m.assert_not_called()

    def test_no_refresh_if_unauthenticated(self):
        self.assertNoRefresh(FakeRequest(is_authenticated=False))

    def test_no_refresh_if_no_uaa_expiry(self):
        self.assertNoRefresh(FakeRequest())

    def test_no_refresh_if_token_not_expired(self):
        self.assertNoRefresh(FakeRequest(session={"uaa_expiry": 150}), time=100)

    def test_no_refresh_if_view_func_is_exempt(self):
        self.assertNoRefresh(
            FakeRequest(session={"uaa_expiry": 150}),
            time=200,
            view_func=uaa_refresh_exempt(noop),
        )

    @patch.object(middleware, "logout")
    @patch.object(middleware, "update_access_token_with_refresh_token")
    def test_logout_when_refresh_fails(self, refresh, logout):
        refresh.return_value = None
        req = FakeRequest(session={"uaa_expiry": 150})
        with patch("time.time", return_value=200):
            UaaRefreshMiddleware().process_view(req, noop, [], {})
            logout.assert_called_once_with(req)

    @patch.object(middleware, "logout")
    @patch.object(middleware, "update_access_token_with_refresh_token")
    def test_no_logout_when_refresh_succeeds(self, refresh, logout):
        refresh.return_value = "I am a fake access token"
        req = FakeRequest(session={"uaa_expiry": 150})
        with patch("time.time", return_value=200):
            UaaRefreshMiddleware().process_view(req, noop, [], {})
            logout.assert_not_called()

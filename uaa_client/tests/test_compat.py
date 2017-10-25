from django.test import SimpleTestCase

from uaa_client.compat import is_user_authenticated


class FakeUser:
    def __init__(self, is_authenticated):
        self.is_authenticated = is_authenticated


class CompatTests(SimpleTestCase):
    def test_is_user_authenticated_works_on_django_1(self):
        self.assertTrue(is_user_authenticated(FakeUser(lambda: True)))
        self.assertFalse(is_user_authenticated(FakeUser(lambda: False)))

    def test_is_user_authenticated_works_on_django_2(self):
        self.assertTrue(is_user_authenticated(FakeUser(True)))
        self.assertFalse(is_user_authenticated(FakeUser(False)))

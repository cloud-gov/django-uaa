from django.test import SimpleTestCase, override_settings
from django.core.exceptions import ImproperlyConfigured

from .. import configuration


def validate_configuration():
    configuration.validate_configuration(use_earliest_debug_setting=False)


class ConfigurationTests(SimpleTestCase):
    @override_settings(
        UAA_CLIENT_ID=None,
        UAA_CLIENT_SECRET=None,
        UAA_AUTH_URL=None,
        UAA_TOKEN_URL=None,
    )
    def test_err_if_no_settings_are_defined(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_configuration()

    @override_settings(
        UAA_CLIENT_ID="", UAA_CLIENT_SECRET="", UAA_AUTH_URL="", UAA_TOKEN_URL=""
    )
    def test_err_if_settings_are_empty(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_configuration()

    @override_settings(
        UAA_CLIENT_ID=1, UAA_CLIENT_SECRET=2, UAA_AUTH_URL=3, UAA_TOKEN_URL=4
    )
    def test_err_if_settings_are_not_strings(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_configuration()

    @override_settings(
        UAA_CLIENT_ID="foo",
        UAA_CLIENT_SECRET="bar",
        UAA_AUTH_URL="https://boop",
        UAA_TOKEN_URL="https://blap",
    )
    def test_nothing_raised_if_prod_settings_are_ok(self):
        validate_configuration()

    @override_settings(
        UAA_CLIENT_ID="foo",
        UAA_CLIENT_SECRET="bar",
        UAA_AUTH_URL="fake:",
        UAA_TOKEN_URL="fake:",
        DEBUG=True,
    )
    def test_nothing_raised_if_fake_backend_used_in_dev_mode(self):
        validate_configuration()

    @override_settings(
        UAA_CLIENT_ID="foo",
        UAA_CLIENT_SECRET="bar",
        UAA_AUTH_URL="fake:",
        UAA_TOKEN_URL="https://blap",
        DEBUG=True,
    )
    def test_err_raised_if_only_one_url_is_fake(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_configuration()

    @override_settings(
        UAA_CLIENT_ID="foo",
        UAA_CLIENT_SECRET="bar",
        UAA_AUTH_URL="fake:",
        UAA_TOKEN_URL="fake:",
        DEBUG=False,
    )
    def test_err_if_fake_uaa_used_but_debug_is_false(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_configuration()

    @override_settings(
        UAA_CLIENT_ID="foo",
        UAA_CLIENT_SECRET="bar",
        UAA_AUTH_URL="http://boop",
        UAA_TOKEN_URL="http://blap",
        DEBUG=False,
    )
    def test_err_if_prod_urls_are_not_https(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_configuration()

    @override_settings(
        UAA_CLIENT_ID="foo",
        UAA_CLIENT_SECRET="bar",
        UAA_AUTH_URL="https://boop",
        UAA_TOKEN_URL="https://blap",
        AUTHENTICATION_BACKENDS=["django.contrib.auth.backends.ModelBackend"],
    )
    def test_err_if_auth_backends_are_invalid(self):
        with self.assertRaises(ImproperlyConfigured):
            validate_configuration()

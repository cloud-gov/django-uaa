from unittest.mock import patch

from django.test import TestCase, override_settings
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.conf.urls import url

from ..decorators import staff_login_required


@staff_login_required
def staff_only_view(request):
    return HttpResponse("ok")


@staff_login_required(login_url="/custom_login_url/")
def staff_only_view_with_custom_login_url(request):
    return HttpResponse("ok")


urlpatterns = [
    url(r"^staff_only_view/$", staff_only_view),
    url(
        r"^staff_only_view_with_custom_login_url/$",
        staff_only_view_with_custom_login_url,
    ),
]


@override_settings(ROOT_URLCONF=__name__, LOGIN_URL="/log_me_in/")
class StaffLoginRequiredTests(TestCase):
    url = "/staff_only_view/"
    redirect_url = "/log_me_in/?next=/staff_only_view/"

    def setUp(self):
        patcher = patch("uaa_client.decorators.logger")
        self.logger = patcher.start()
        self.addCleanup(patcher.stop)

    def login(self, is_staff=False):
        user = User.objects.create_user(username="foo", email="foo@bar.gov")
        if is_staff:
            user.is_staff = True
            user.save()
        self.client.force_login(user)
        return user

    def test_redirects_to_login(self):
        res = self.client.get(self.url)
        self.assertEqual(302, res.status_code)
        self.assertEquals(res["Location"], self.redirect_url)
        self.logger.info.assert_called_once_with(
            "Unauthenticated user has attempted to access is_staff view"
        )

    def test_staff_user_is_permitted(self):
        self.login(is_staff=True)
        res = self.client.get(self.url)
        self.assertEqual(200, res.status_code)
        self.assertEqual(b"ok", res.content)
        self.logger.info.assert_called_once_with(
            "User with id 1 (foo@bar.gov) has passed is_staff check"
        )

    def test_non_staff_user_is_denied(self):
        self.login(is_staff=False)
        res = self.client.get(self.url)
        self.assertEqual(403, res.status_code)
        self.logger.info.assert_called_once_with(
            "User with id 1 (foo@bar.gov) is authenticated but "
            "has not passed is_staff check"
        )


class CustomLoginUrlTests(StaffLoginRequiredTests):
    url = "/staff_only_view_with_custom_login_url/"
    redirect_url = "/custom_login_url/?" "next=/staff_only_view_with_custom_login_url/"

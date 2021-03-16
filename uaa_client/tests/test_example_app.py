import sys
import subprocess
from pathlib import Path
from unittest import TestCase, SkipTest


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
EXAMPLE_APP_DIR = ROOT_DIR / "example"


class ExampleAppTests(TestCase):
    def test_example_app_tests_work(self):
        # This is partly a regression test for the following issue:
        #
        # https://github.com/18F/cg-django-uaa/issues/18

        if not EXAMPLE_APP_DIR.exists():
            # We're being run from an installed package or something, just
            # skip this test.
            raise SkipTest("Example app dir unavailable to distribution")

        subprocess.check_output(
            [sys.executable, "manage.py", "test"],
            stderr=subprocess.STDOUT,
            cwd=str(EXAMPLE_APP_DIR),
        )

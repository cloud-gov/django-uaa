import sys
import subprocess
from pathlib import Path
from unittest import TestCase


ROOT_DIR = Path(__file__).resolve().parent.parent.parent
EXAMPLE_APP_DIR = ROOT_DIR / 'example'


class ExampleAppTests(TestCase):
    def test_example_app_tests_work(self):
        # This is partly a regression test for the following issue:
        #
        # https://github.com/18F/cg-django-uaa/issues/18

        subprocess.check_output(
            [sys.executable, 'manage.py', 'test'],
            stderr=subprocess.STDOUT,
            cwd=str(EXAMPLE_APP_DIR)
        )

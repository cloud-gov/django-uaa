import os
from unittest import TestCase

from uaa_client import VERSION

CONF_PY_PATH = os.path.join('docs', 'conf.py')
CONF_PY_GLOBALS = {}

with open(CONF_PY_PATH, 'r', encoding='utf-8') as f:
    exec(f.read(), CONF_PY_GLOBALS)


class ConfPyTests(TestCase):
    def test_version_is_consistent(self):
        self.assertEqual(CONF_PY_GLOBALS['version'], VERSION)

    def test_release_is_consistent(self):
        self.assertEqual(CONF_PY_GLOBALS['release'], VERSION)

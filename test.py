"""
This holds a couple handy commands that were in setup.py
before we moved to static builds using setup.cfg
"""
import os
import sys
import distutils.cmd
from setuptools import setup, find_packages
import subprocess

from uaa_client import VERSION



class SimpleCommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class ManualTestCommand(SimpleCommand):
    description = "Run example app in a Docker container for manual testing."

    SDIST_PATH = os.path.join("dist", "cg-django-uaa-{}.tar.gz".format(VERSION))

    def run(self):
        if not os.path.exists(self.SDIST_PATH):
            print("Please run 'python setup.py sdist' first.")
            sys.exit(1)

        import django

        django_version = django.get_version()
        tag_name = "cg-django-uaa"

        subprocess.check_call(
            [
                "docker",
                "build",
                "--build-arg",
                "version={}".format(VERSION),
                "--build-arg",
                "django_version={}".format(django_version),
                "-t",
                tag_name,
                ".",
            ]
        )
        subprocess.check_call(
            ["docker", "run", "-it", "-p", "8000:8000", "--rm", tag_name]
        )


class DevDocsCommand(SimpleCommand):
    description = "Run development server for documentation"

    def run(self):
        subprocess.check_call(
            ["sphinx-autobuild", ".", "_build_html", "-p", "8001"], cwd="docs"
        )



setup(
    cmdclass={
        "devdocs": DevDocsCommand,
        "manualtest": ManualTestCommand,
    },
)

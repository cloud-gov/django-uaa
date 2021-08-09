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


class UltraTestCommand(SimpleCommand):
    description = "Run tests, code coverage, linting, etc."

    def run(self):
        print("Running tests...")
        subprocess.check_call(["coverage", "run", "setup.py", "test"])
        print("Running mypy...")
        subprocess.check_call([sys.executable, "-m", "mypy", "uaa_client"])
        print("Ensuring code coverage is at 100%...")
        subprocess.check_call(["coverage", "report", "-m"])
        print("Success!")


setup(
    name="cg-django-uaa",
    cmdclass={
        "devdocs": DevDocsCommand,
        "ultratest": UltraTestCommand,
        "manualtest": ManualTestCommand,
    },
    zip_safe=False,
    version=VERSION,
    description="A cloud.gov UAA authentication backend for Django",
    long_description=open("README.rst", "r", encoding="utf-8").read(),
    author="Atul Varma",
    author_email="atul.varma@gsa.gov",
    license="Public Domain",
    url="https://github.com/cloud-gov/cg-django-uaa",
    package_dir={"uaa_client": "uaa_client"},
    include_package_data=True,
    packages=find_packages(),
    install_requires=["django>=2.2,<3.3", "PyJWT>=1.4.2,<2.0", "requests>=2.11.0"],
    test_suite="uaa_client.runtests.run_tests",
    tests_require=open("requirements-tests.txt", "r").read().strip().split("\n"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Framework :: Django :: 3.2",
        "Intended Audience :: Developers",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Utilities",
    ],
)

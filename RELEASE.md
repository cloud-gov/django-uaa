# Releasing

Here's how to issue a new release:

1. Bump the version number in `uaa_client/__init__.py`.

1. Move the "unreleased" section to a new version entry in
   `CHANGELOG.md`.

1. [Follow the development instructions](https://cg-django-uaa.readthedocs.io/en/main/developing.html) to:

   - [Run the unit tests](https://cg-django-uaa.readthedocs.io/en/main/developing.html#running-tests)
   - [Run the example app test](https://cg-django-uaa.readthedocs.io/en/main/developing.html#using-the-example-app)

1. Commit and push your changes with a commit message like
   "Bump version to v1.0.4."

1. Tag your version and push it to GitHub. For instance, if you're
   releasing v1.0.4, do:

   ```shell
   git tag -a v1.0.4
   git push origin v1.0.4
   ```

   When running `git tag`, you'll be prompted for a tag
   message. Consider copy-pasting the version notes from
   `CHANGELOG.md` for this, as whatever you enter will
   show up on the [GitHub releases page][].

1. If you haven't already done so, create a `~/.pypirc` file
   with the following content:

   ```conf
   [distutils]
   index-servers =
       pypi

   [pypi]
   repository: https://www.python.org/pypi
   username: 18f
   password: <your password>
   ```

1. Run `python -m twine upload dist/*`.  The new release should now
   be visible on [pypi][].

[GitHub releases page]: https://github.com/18F/cg-django-uaa/releases
[pypi]: https://pypi.python.org/pypi/cg-django-uaa

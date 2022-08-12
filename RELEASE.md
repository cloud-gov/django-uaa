# Releasing

Here's how to issue a new release:

1. Bump the version number in `uaa_client/__init__.py`.

2. Move the "unreleased" section to a new version entry in
   `CHANGELOG.md`.

3. From the project root, install dependencies and run automated tests:

   ```shell
   tox
   ```

4. Run the following to ensure that everything builds and
   installs OK in an isolated environment:

   ```shell
   rm -rf dist build
   python -m build
   python test.py manualtest
   ```

   You should be able to visit <http://localhost:8000> and log in
   as foo@example.org without any problems.

5. Commit and push your changes with a commit message like
   "Bump version to v1.0.4."

6. Tag your version and push it to GitHub. For instance, if you're
   releasing v1.0.4, do:

   ```shell
   git tag -a v1.0.4
   git push origin v1.0.4
   ```

   When running `git tag`, you'll be prompted for a tag
   message. Consider copy-pasting the version notes from
   `CHANGELOG.md` for this, as whatever you enter will
   show up on the [GitHub releases page][].

7. If you haven't already done so, create a `~/.pypirc` file
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

8. Run `python -m twine upload dist/*`.  The new release should now
   be visible on [pypi][].

[GitHub releases page]: https://github.com/18F/cg-django-uaa/releases
[pypi]: https://pypi.python.org/pypi/cg-django-uaa

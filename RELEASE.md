Here's how to issue a new release.

1. Bump the version number in `uaa_client/__init__.py`.

2. Move the "unreleased" section to a new version entry in
   `CHANGELOG.md`.

3. Commit and push your changes with a commit message like
   "Bump version to v1.0.4."

4. Tag your version and push it to GitHub. For instance, if you're
   releasing v1.0.4, do:

   ```
   git tag -a v1.0.4
   git push origin v1.0.4
   ```

   When running `git tag`, you'll be prompted for a tag
   message. Consider copy-pasting the version notes from
   `CHANGELOG.md` for this, as whatever you enter will
   show up on the [GitHub releases page][].

5. If you haven't already done so, create a `~/.pypirc` file
   with the following content:

   ```
   [distutils]
   index-servers =
       pypi

   [pypi]
   repository: https://www.python.org/pypi
   username: 18f
   password: <your password>
   ```

6. Run `python setup.py sdist upload`.  The new release should now
   be visible on [pypi][].

[GitHub releases page]: https://github.com/18F/cg-django-uaa/releases
[pypi]: https://pypi.python.org/pypi/cg-django-uaa

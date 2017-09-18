# Change log

All notable changes to this project will be documented in this file,
which uses the format described in
[keepachangelog.com](http://keepachangelog.com/). This project adheres
to [Semantic Versioning](http://semver.org/).

## [Unreleased][unreleased]

## [1.2.0][] - 2017-09-18

* An info-level message is logged when users authenticate.

## [1.1.0][] - 2017-06-20

* The library no longer raises spurious `ImproperlyConfigured` errors
  during test suite runs.

* Added an optional `UAA_APPROVED_DOMAINS` setting, allowing users to
  be auto-created if their email is from an approved list of domains. See
  the quick start for more details.

* Added more documented methods to `UaaBackend` for easier customization.
  Static methods have also been converted to class methods for easier
  subclassing.

## [1.0.1][] - 2017-04-20

This is a hotfix release to fix a broken pypi build.

## [1.0.0][] - 2017-04-20

### Added

* Added support for automatic refreshing of access tokens, which
  is required for security. This involves adding
  `uaa_client.middleware.UaaRefreshMiddleware` to your
  middleware setting, after Django's session and authentication
  middleware. For more details, see the quick start guide.

* The example app now supports an optional `settings_local.py`,
  so it's easy to e.g. connect to the real cloud.gov for manual
  testing.

## 0.0.1 - 2017-02-02

Initial release.

[unreleased]: https://github.com/18F/cg-django-uaa/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/18F/cg-django-uaa/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/18F/cg-django-uaa/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/18F/cg-django-uaa/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/18F/cg-django-uaa/compare/v0.0.1...v1.0.0

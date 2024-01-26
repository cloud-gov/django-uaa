# Change log

All notable changes to this project will be documented in this file,
which uses the format described in
[keepachangelog.com](http://keepachangelog.com/). This project adheres
to [Semantic Versioning](http://semver.org/).

## [Unreleased][unreleased]

## [2.1.5][] - 2024-01-26

* Update Django dependency to `>=4.0,<5.0`

## [2.1.4][] - 2022-08-16

* Update PyJWT version to >= `2.4.0` to [address vulnerability](https://security.snyk.io/vuln/SNYK-PYTHON-PYJWT-2840625)

## [2.1.3][] - 2021-08-10

* Fix packaging issue

## [2.1.2][] - 2021-08-10

* Added support for Django 3.2 LTS

## [2.1.1][] - 2020-03-16

* correctly specify django versions in setup.py
* code formatting

## [2.1.0][] - 2020-03-16

* Added support for Django 3.0 and 3.1
* Pinned upper version for PyJWT to fix install issues

## [2.0.0][] - 2019-06-24

* Added support for Django 2.2

* Removed support for Django 2.0 and 1.X

## [1.3.0][] - 2017-03-22

* Added support for Django 2.0.

* Added the `uaa_client.decorators.staff_login_required` decorator
  and a "Fixing admin login" section to the quick start guide
  that documents how to use it.

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

[unreleased]: https://github.com/cloud-gov/cg-django-uaa/compare/v2.1.5...HEAD
[2.1.5]: https://github.com/cloud-gov/cg-django-uaa/compare/v2.1.4...v2.1.5
[2.1.4]: https://github.com/cloud-gov/cg-django-uaa/compare/v2.1.3...v2.1.4
[2.1.3]: https://github.com/cloud-gov/cg-django-uaa/compare/v2.1.2...v2.1.3
[2.1.2]: https://github.com/cloud-gov/cg-django-uaa/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.com/cloud-gov/cg-django-uaa/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.com/cloud-gov/cg-django-uaa/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/cloud-gov/cg-django-uaa/compare/v1.3.0...v2.0.0
[1.3.0]: https://github.com/cloud-gov/cg-django-uaa/compare/v1.2.0...v1.3.0
[1.2.0]: https://github.com/cloud-gov/cg-django-uaa/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/cloud-gov/cg-django-uaa/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/cloud-gov/cg-django-uaa/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/cloud-gov/cg-django-uaa/compare/v0.0.1...v1.0.0

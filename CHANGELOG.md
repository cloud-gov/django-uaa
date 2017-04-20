# Change log

All notable changes to this project will be documented in this file,
which uses the format described in
[keepachangelog.com](http://keepachangelog.com/). This project adheres
to [Semantic Versioning](http://semver.org/).

## [Unreleased][unreleased]

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

[unreleased]: https://github.com/18F/cg-django-uaa/compare/v0.0.1...HEAD

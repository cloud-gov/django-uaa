# Authentication backends

## *class* **classuaa_client.authentication.UaaBackend**

Custom auth backend for Cloud Foundry / cloud.gov User Account and Authentication (UAA) servers.

This inherits from **`django.contrib.auth.backends.ModelBackend`** so that the superclass can provide all authorization methods.

### *classmethod* **create_user_with_email**(*email*)

Create and return a new User with the given email.

Assumes the given email address has already been approved for auto-creation.

By default, the new user has a username set to the email address, but subclasses may override this method if needed.

### *classmethod* **get_user_by_email**(*email*)

Return a **`django.contrib.auth.models.User`** with the given email address. If no user can be found, return `None`.

The default implementation attempts to find an existing user with the given case-insensitive email address. If no such user exists, `should_create_user_for_email()` is consulted to determine whether the user should be auto-created; if so, `create_user_with_email()` is used to auto-create the user. Otherwise, `None` is returned.

Subclasses may override this method to account for different kinds of security policies for logins.

### *classmethod* **should_create_user_for_email**(*email*)

Returns whether or not a new user with the given email can be created.

The default implementation consults whether the domain of the email address is in the list of approved domains, but subclasses may override this method if needed.

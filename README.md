# django-duo-universal-auth

A lightweight middleware application that adds a layer on top of any number of existing authentication backends, enabling 2FA with the user's Duo account using the [Universal Prompt](https://guide.duo.com/universal-prompt) after signing in with your Django application.

**Note:** In order to interface this middleware with Duo, you must create a new [Duo Web SDK](https://duo.com/docs/duoweb) application from within your organization's Duo Admin Portal and enable the "Show new Universal Prompt" setting. You will acquire a Client ID, Client Secret, and API Hostname, of which you will include in your `settings.py` file in the format listed below. It is strongly recommended not to hardcode these values in the settings file itself.

From [Duo's documentation for protecting applications](https://duo.com/docs/protecting-applications):
 > **Treat your Secret key or Client ID like a password**
The security of your Duo application is tied to the security of your Secret key (skey) or Client secret (client_secret). Secure it as you would any sensitive credential. Don't share it with unauthorized individuals or email it to anyone under any circumstances!

## Installation

To install the middleware application, use the following `pip` command (or equivalent for your package manager application):

```sh
pip install django-duo-universal-auth
```

### Sample Configuration (in your `settings.py` file)

First, add the package to your `INSTALLED_APPS` list variable:

```python
INSTALLED_APPS = [
    # ...
    'duo_universal_auth', # Add this!
]
```

Next, add the path for the middleware application to the `MIDDLEWARE` list variable:

```python
MIDDLEWARE = [
    # ...
    'duo_universal_auth.middleware.DuoUniversalAuthMiddleware', # Add this!
]
```

Then, add a new `DUO_UNIVERSAL_AUTH` configuration variable:

```python
DUO_UNIVERSAL_AUTH = {
    'MAIN': {
        'DUO_HOST': '<api_hostname>',
        'CLIENT_ID': '<client_id>',
        'CLIENT_SECRET': '<client_secret>',
        'AUTH_BACKENDS': [
            'django.contrib.auth.backends.ModelBackend',
        ],
        'FAIL_ACTION': 'CLOSED'
    }
}
```

## Duo API Callback Setup

**Note:** This step allows the application to communicate with Duo. If the view is not registered, the application will raise a `NoReverseMatch` error upon starting the Duo authentication flow.

To create the callback for the API to communicate with, you must add an entry to your `urlpatterns` variable from within your application's `urls.py` file (with any prepending path you choose):

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path('duo/', include('duo_universal_auth.urls')), # Add this!
]
```

## Configuration Docs

Configurations for each Duo application are specified within individual dictionary objects inside a parent `DUO_UNIVERSAL_AUTH` dictionary each containing the following values:

#### `DUO_HOST`
##### Required: True

Represents the API Hostname for your organization's Duo API.
```python
'DUO_HOST': 'api-XXXXXXX.duosecurity.com'
```

#### `CLIENT_ID`
##### Required: True

Represents the Client ID for your application registered from within the Duo Admin Portal.
```python
'CLIENT_ID': 'DIXXXXXXXXXXXXXXXXXX'
```

#### `CLIENT_SECRET`
##### Required: True

Represents the Client Secret for your application registered from within the Duo Admin Portal.
```python
'CLIENT_SECRET': 'deadbeefdeadbeefdeadbeefdeadbeefdeadbeef'
```

#### `AUTH_BACKENDS`
##### Required: True

A list of authentication backends that the middleware will work with for the specific application. The Duo authentication middleware will only execute upon a successful authentication result from one of these backends.
```python
'AUTH_BACKENDS': [
    'django.contrib.auth.backends.ModelBackend',
]
```

#### `FAIL_ACTION`
##### Required: False (Default: `'CLOSED'`)

How the middleware should respond should the Duo authentication server be unavailable (from failing the preliminary health check).

 - `'CLOSED'`: Log out the user and return to the login page, disallowing any authentication while Duo servers are unavailable.
 - `'OPEN'`: Temporarily bypass Duo authentication until the Duo servers become available upon a future authentication attempt.
```python
'FAIL_ACTION': 'CLOSED'
```

#### `USERNAME_REMAP_FUNCTION`
##### Required: False

An optional one-argument function that takes in the current Django [`HttpRequest`](https://docs.djangoproject.com/en/4.0/ref/request-response/#httprequest-objects) object and returns the current authenticated user's username to send for Duo authentication. If unspecified, the username from [`HttpRequest.user`](https://docs.djangoproject.com/en/4.0/ref/request-response/#django.http.HttpRequest.user) will be used.

```python
'USERNAME_REMAP_FUNCTION': lambda r: r.user.username  # Mimics default behavior
```

## Post-Authentication Redirect
Once successfully authenticated with Duo, the middleware will automatically redirect the user to the path specified in the `DUO_NEXT_URL` session variable, falling back to the `LOGIN_REDIRECT_URL` settings variable if it is not present. This value is automatically assigned in the middleware before redirecting to Duo.

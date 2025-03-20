# Django-Doorkeeper

Django-Doorkeeper is a pluggable Django middleware that forces every visitor to a site to enter a password before viewing any pages. The password is the same for every user. Doorkeeper status is stored in a cookie and does not need to be re-entered on subsequent pageviews.

Doorkeeper **IS NOT SECURE** and should not be used for security purposes. Its intent is to protect a site from casual lookie-loos and stray bots. Under some circumstances you might do this with .htaccess and HTTP Basic Auth if your site is fronted with Nginx / Apache / etc. When it's not, this is a simple substitute.

Individual users can be exempted from the password prompt. See [configuration documentation](./docs/configuration.md) for more information.

## Installation

```sh
pip install git+ssh://git@github.com:triopter/django-doorkeeper.git
```

Then configure as documented.

## Configuration

See [configuration documentation](./docs/configuration.md).

## Demo App

This repository includes a demo application to showcase Doorkeeper's functionality. To run the demo:

1. Navigate to the example directory:

   ```sh
   cd example
   ```

2. Install Django and doorkeeper:

   ```sh
   pip install django
   pip install git+ssh://git@github.com:triopter/django-doorkeeper.git
   ```

3. Run migrations and start the demo server:

   ```sh
   python manage.py migrate
   python manage.py runserver
   ```

4. Visit http://127.0.0.1:8000/ in your browser. You'll be prompted for the password (default: "demo_password").

5. To see a page that bypasses Doorkeeper, visit http://127.0.0.1:8000/public/

## Testing

```sh
python runtests.py
```

## Compatibility

Doorkeeper has been tested with Python 3.13 and Django 5.1 but will almost certainly work on many earlier and later versions. Maybe if anyone every uses this, someday I'll get around to adding Tox and a test matrix.

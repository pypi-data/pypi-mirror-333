from django.test import override_settings

from doorkeeper.helpers import get_doorkeeper_setting
from doorkeeper.tests.base import DoorkeeperTestCase


class CookiesTestCase(DoorkeeperTestCase):
    """Tests for the cookie behavior."""

    def test_cookie_creation(self):
        """Test that a cookie is created with correct attributes after authentication."""
        # Authenticate
        response = self.authenticate()

        # Check that the cookie exists in the response
        cookie_name = get_doorkeeper_setting("COOKIE_NAME")
        self.assertIn(cookie_name, response.cookies)

        # Check cookie attributes
        cookie = response.cookies[cookie_name]
        self.assertEqual(cookie["path"], "/")  # Default path
        self.assertTrue(cookie["httponly"])  # Default httponly

    @override_settings(
        DOORKEEPER={"ENABLED": True, "PASSWORD": "sesame", "DEFAULT_REDIRECT_URL": "/", "COOKIE_NAME": "custom_cookie"}
    )
    def test_custom_cookie_name(self):
        """Test that a custom cookie name is used when configured."""
        # Authenticate
        response = self.authenticate()

        # Check that the cookie with custom name exists
        self.assertIn("custom_cookie", response.cookies)

        # Should be able to access protected content
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)

    @override_settings(
        DOORKEEPER={"ENABLED": True, "PASSWORD": "sesame", "DEFAULT_REDIRECT_URL": "/", "COOKIE_PATH": "/custom-path/"}
    )
    def test_custom_cookie_path(self):
        """Test that a custom cookie path is used when configured."""
        # Authenticate
        response = self.authenticate()

        # Check that the cookie has the custom path
        cookie_name = get_doorkeeper_setting("COOKIE_NAME")
        self.assertEqual(response.cookies[cookie_name]["path"], "/custom-path/")

    def test_cookie_removal(self):
        """Test that the cookie is removed when exiting."""
        # Authenticate first
        self.authenticate()

        # Then exit
        response = self.client.post(self.exit_url)

        # Check that the cookie is deleted
        cookie_name = get_doorkeeper_setting("COOKIE_NAME")
        self.assertIn(cookie_name, response.cookies)
        self.assertEqual(response.cookies[cookie_name]["max-age"], 0)

        # Should no longer have access to protected pages
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, self.entrance_url + f"?doorkeeper_next_url={self.protected_url}")

    @override_settings(
        DOORKEEPER={"ENABLED": True, "PASSWORD": "sesame", "DEFAULT_REDIRECT_URL": "/", "COOKIE_AGE": 3600}
    )
    def test_cookie_age(self):
        """Test that the cookie age is set correctly."""
        # Authenticate
        response = self.authenticate()

        # Check that the cookie has the correct max age
        cookie_name = get_doorkeeper_setting("COOKIE_NAME")
        self.assertEqual(response.cookies[cookie_name]["max-age"], 3600)

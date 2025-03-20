from django.test import override_settings

from doorkeeper.tests.base import DoorkeeperTestCase


class RedirectsTestCase(DoorkeeperTestCase):
    """Tests for the redirection behavior."""

    def test_original_url_redirect(self):
        """Test that users are redirected to their original destination after authentication."""
        # First try to access a protected page
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, self.entrance_url + f"?{self.next_url_param_name}={self.protected_url}")

        # Then authenticate
        response = self.authenticate(next_url=self.protected_url)

        # Should redirect to the original URL
        self.assertRedirects(response, self.protected_url)

    def test_default_redirect(self):
        """Test that users are redirected to DEFAULT_REDIRECT_URL when no original URL exists."""
        # Access the entrance page directly
        response = self.client.get(self.entrance_url)
        self.assertEqual(response.status_code, 200)

        # Authenticate without a next URL
        response = self.authenticate()

        # Should redirect to the default URL
        self.assertRedirects(response, "/")

    @override_settings(
        DOORKEEPER={
            "ENABLED": True,
            "PASSWORD": "sesame",
            "DEFAULT_REDIRECT_URL": "/",
            "NEXT_URL_PARAM_NAME": "custom_next",
        }
    )
    def test_custom_next_param(self):
        """Test that URL tracking works with a custom parameter name."""
        # First try to access a protected page
        response = self.client.get(self.protected_url)
        # Should redirect with the custom parameter name
        self.assertRedirects(response, self.entrance_url + f"?custom_next={self.protected_url}")

        # Then authenticate
        self.next_url_param_name = "custom_next"  # Update the parameter name for this test
        response = self.authenticate(next_url=self.protected_url)

        # Should redirect to the original URL
        self.assertRedirects(response, self.protected_url)

    def test_exit_redirect(self):
        """Test that users are redirected to EXIT_REDIRECT_URL when exiting."""
        # Authenticate first
        self.authenticate(next_url=self.protected_url)

        # Then exit
        response = self.client.post(self.exit_url)

        # Should redirect to the entrance URL (default EXIT_REDIRECT_URL)
        self.assertRedirects(response, self.entrance_url)

        # Should no longer have access to protected pages
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, self.entrance_url + f"?{self.next_url_param_name}={self.protected_url}")

    @override_settings(
        DOORKEEPER={
            "ENABLED": True,
            "PASSWORD": "sesame",
            "DEFAULT_REDIRECT_URL": "/",
            "EXIT_REDIRECT_URL": "/public/",
            "BYPASS_PATHS": ["/public/"],
        }
    )
    def test_custom_exit_redirect(self):
        """Test that users are redirected to a custom EXIT_REDIRECT_URL when exiting."""
        # Authenticate first
        self.authenticate(next_url=self.protected_url)

        # Then exit
        response = self.client.post(self.exit_url)

        # Check that the response redirects to the public URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.public_url)

        # Follow the redirect manually with follow=True
        response = self.client.get(self.public_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Public content")

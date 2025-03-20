from django.test import override_settings

from doorkeeper.tests.base import DoorkeeperTestCase


class AuthenticationTestCase(DoorkeeperTestCase):
    """Tests for the basic authentication flow."""

    def test_unauthenticated_redirect(self):
        """Test that unauthenticated users are redirected to the password prompt."""
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, self.entrance_url + f"?{self.next_url_param_name}={self.protected_url}")

    def test_successful_authentication(self):
        """Test that submitting the correct password grants access."""
        # First try to access a protected page
        self.client.get(self.protected_url)

        # Then authenticate with the correct password
        response = self.authenticate(next_url=self.protected_url)

        # Should redirect to the protected page
        self.assertRedirects(response, self.protected_url)

        # Now we should be able to access the protected page directly
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Protected content")

    def test_failed_authentication(self):
        """Test that submitting an incorrect password keeps the user at the prompt."""
        # First try to access a protected page
        self.client.get(self.protected_url)

        # Then authenticate with an incorrect password
        response = self.authenticate(password="wrong_password", next_url=self.protected_url)

        # Should stay at the entrance page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "doorkeeper/doorkeeper_entrance.html")

        # Should still be redirected when trying to access protected content
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, self.entrance_url + f"?{self.next_url_param_name}={self.protected_url}")

    def test_persistent_authentication(self):
        """Test that authentication persists across multiple requests."""
        # Authenticate
        self.authenticate(next_url=self.protected_url)

        # Access multiple protected pages
        response1 = self.client.get(self.protected_url)
        self.assertEqual(response1.status_code, 200)

        # Create a different protected URL path and try to access it
        different_protected_url = "/protected/another/"
        response2 = self.client.get(different_protected_url)
        # This should 404 but not redirect to doorkeeper
        self.assertEqual(response2.status_code, 404)

    @override_settings(DOORKEEPER={"ENABLED": False, "PASSWORD": "sesame", "DEFAULT_REDIRECT_URL": "/"})
    def test_disabled_doorkeeper(self):
        """Test that when doorkeeper is disabled, all pages are accessible."""
        # Should be able to access protected content without authentication
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Protected content")

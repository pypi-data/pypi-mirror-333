from django.test import override_settings

from doorkeeper.tests.base import DoorkeeperTestCase


class BypassTestCase(DoorkeeperTestCase):
    """Tests for the bypass functionality."""

    def test_exempt_decorator(self):
        """Test that views with the doorkeeper_exempt decorator are accessible without authentication."""
        # Should be able to access exempt view without authentication
        response = self.client.get(self.exempt_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Exempt content")

        # But protected views should still require authentication
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, self.entrance_url + f"?{self.next_url_param_name}={self.protected_url}")

    @override_settings(
        DOORKEEPER={"ENABLED": True, "PASSWORD": "sesame", "DEFAULT_REDIRECT_URL": "/", "BYPASS_PATHS": ["/public/"]}
    )
    def test_bypass_paths(self):
        """Test that paths in BYPASS_PATHS are accessible without authentication."""
        # Should be able to access public view without authentication
        response = self.client.get(self.public_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Public content")

        # But protected views should still require authentication
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, self.entrance_url + f"?{self.next_url_param_name}={self.protected_url}")

    @override_settings(
        DOORKEEPER={"ENABLED": True, "PASSWORD": "sesame", "DEFAULT_REDIRECT_URL": "/", "BYPASS_PATHS": ["/protected/"]}
    )
    def test_bypass_protected_path(self):
        """Test that protected paths can be bypassed if added to BYPASS_PATHS."""
        # Should be able to access protected view without authentication if it's in BYPASS_PATHS
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Protected content")

    @override_settings(
        DOORKEEPER={
            "ENABLED": True,
            "PASSWORD": "sesame",
            "DEFAULT_REDIRECT_URL": "/",
            "BYPASS_PATHS": ["/favicon.ico"],
        }
    )
    def test_default_bypass_paths(self):
        """Test that default bypass paths work."""
        # Should be able to access favicon.ico without authentication
        response = self.client.get("/favicon.ico")
        # This will 404 but should not redirect to doorkeeper
        self.assertEqual(response.status_code, 404)

        # But protected views should still require authentication
        response = self.client.get(self.protected_url)
        self.assertRedirects(response, self.entrance_url + f"?{self.next_url_param_name}={self.protected_url}")

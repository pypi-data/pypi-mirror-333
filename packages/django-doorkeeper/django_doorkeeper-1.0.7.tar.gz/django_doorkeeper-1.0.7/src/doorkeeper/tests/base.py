from django.test import Client, TestCase, override_settings


class DoorkeeperTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.protected_url = "/protected/"
        self.public_url = "/public/"
        self.exempt_url = "/exempt/"
        self.entrance_url = "/doorkeeper/entrance/"
        self.exit_url = "/doorkeeper/exit/"
        self.next_url_param_name = "doorkeeper_next_url"

    def authenticate(self, password="sesame", next_url=None):
        """Helper method to authenticate with doorkeeper"""
        data = {"password": password}
        url = self.entrance_url

        if next_url:
            if "?" in url:
                url += f"&{self.next_url_param_name}={next_url}"
            else:
                url += f"?{self.next_url_param_name}={next_url}"

        return self.client.post(url, data)

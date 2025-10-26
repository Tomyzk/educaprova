from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class UsersSmokeTest(TestCase):
    def test_register_and_login_jwt(self):
        # Register
        resp = self.client.post(
            reverse("register"),
            {
                "username": "u1",
                "email": "u1@example.com",
                "password": "SenhaForte123",
                "first_name": "U",
                "last_name": "One",
            },
            content_type="application/json",
        )
        self.assertIn(resp.status_code, (200, 201, 204))

        # Login (email + password)
        resp = self.client.post(
            reverse("token_obtain_pair"),
            {"email": "u1@example.com", "password": "SenhaForte123"},
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("access", resp.json())


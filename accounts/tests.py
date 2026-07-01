from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_signup_creates_user_and_redirects_to_dashboard(self):
        response = self.client.post(
            reverse("accounts:signup"),
            {
                "full_name": "Ada Lovelace",
                "username": "ada",
                "email": "ada@example.com",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:dashboard"))
        self.assertTrue(get_user_model().objects.filter(username="ada").exists())

    def test_login_with_email_succeeds(self):
        user = get_user_model().objects.create_user(
            username="grace",
            email="grace@example.com",
            password="StrongPass123!",
        )

        response = self.client.post(
            reverse("accounts:signin"),
            {"identifier": user.email, "password": "StrongPass123!"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:dashboard"))

    def test_forget_password_page_is_available(self):
        response = self.client.get(reverse("accounts:forgot_password"))
        self.assertEqual(response.status_code, 200)

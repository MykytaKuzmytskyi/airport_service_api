from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airplane
from airport.tests.data_base import DataTestCase

AIRPLANE_URL = reverse("airport:airplane-list")


def detail_url(airplane_id: int) -> str:
    return reverse("airport:airplane-detail", args=[airplane_id])


class AdminAirplaneApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AdminAirplaneApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_airplane_list(self):
        res = self.client.get(AIRPLANE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(self.airplanes), len(res.data))

    def test_get_airplane_detail(self):
        url = detail_url(self.airplane.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], getattr(self.airplane, "name"))

    def test_post_airplane(self):
        payload = {
            "name": "Name",
            "rows": 5,
            "seats_in_row": 5,
            "airplane_type": 1,
        }

        res = self.client.post(AIRPLANE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airplane = Airplane.objects.get(name=payload["name"])
        self.assertIn(airplane, self.airplanes)

    def test_put_airplane(self):
        payload = {
            "name": "New name",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": 1,
        }

        url = detail_url(self.airplane.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["name"], res.data["name"])

    def test_delete_airplane(self):
        url = detail_url(self.airplane.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(res.data)
        self.assertNotIn(self.airplane, self.airplanes)


class AuthenticatedAirplaneApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AuthenticatedAirplaneApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="authenticated@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_airplane_list_forbidden(self):
        res = self.client.get(AIRPLANE_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_airplane_detail_forbidden(self):
        url = detail_url(self.airplane.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_airplane_forbidden(self):
        payload = {
            "name": "Post name",
            "rows": 50,
            "seats_in_row": 50,
            "airplane_type": self.airplane_type,
        }

        res = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_airplane_forbidden(self):
        payload = {
            "name": "New name",
            "rows": 10,
            "seats_in_row": 10,
            "airplane_type": self.airplane_type,
        }

        url = detail_url(self.airplane.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_airplane_forbidden(self):
        url = detail_url(self.airplane.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class UnauthenticatedAirplaneApiTests(DataTestCase):
    def test_get_airplane_list_unauthorized(self):
        res = self.client.get(AIRPLANE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_airplane_detail_unauthorized(self):
        url = detail_url(self.airplane.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_airplane_unauthorized(self):
        payload = {
            "name": "New name",
            "rows": 25,
            "seats_in_row": 25,
            "airplane_type": self.airplane,
        }
        res = self.client.post(AIRPLANE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_airplane_unauthorized(self):
        payload = {
            "name": "New name",
            "rows": 25,
            "seats_in_row": 25,
            "airplane_type": self.airplane_type,
        }

        url = detail_url(self.airplane.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_airplane_unauthorized(self):
        url = detail_url(self.airplane.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import AirplaneType
from airport.tests.data_base import DataTestCase

AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")


def detail_url(airplane_type_id: int) -> str:
    return reverse("airport:airplanetype-detail", args=[airplane_type_id])


class AdminAirplaneTypeApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AdminAirplaneTypeApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_airplane_type_list(self):
        res = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(self.airplane_types), len(res.data))

    def test_get_airplane_type_detail(self):
        url = detail_url(self.airplane_type.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.airplane_type.name)

    def test_post_airplane_type(self):
        payload = {
            "name": "New name",
        }

        res = self.client.post(AIRPLANE_TYPE_URL, payload)
        airplane_type = AirplaneType.objects.get(name=res.data["name"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(airplane_type, key))

    def test_put_airplane_type(self):
        payload = {
            "name": "Updated name",
        }

        url = detail_url(self.airplane_type.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["name"], res.data["name"])

    def test_delete_airplane_type(self):
        url = detail_url(self.airplane_type.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(res.data)
        self.assertNotIn(self.airplane_type, self.airplane_types)


class AuthenticatedAirplaneTypeApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AuthenticatedAirplaneTypeApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="authenticated@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_airplane_type_list_forbidden(self):
        res = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_airplane_type_detail_forbidden(self):
        url = detail_url(self.airplane_type.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_airplane_type_forbidden(self):
        payload = {
            "name": "New name",
        }
        res = self.client.post(AIRPLANE_TYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_airplane_type_forbidden(self):
        payload = {
            "name": "Updated name",
        }

        url = detail_url(self.airplane_type.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_airplane_type_forbidden(self):
        url = detail_url(self.airplane_type.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class UnauthenticatedAirplaneTypeApiTests(DataTestCase):
    def test_get_airplane_type_list_unauthorized(self):
        res = self.client.get(AIRPLANE_TYPE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_airplane_type_detail_unauthorized(self):
        url = detail_url(self.airplane_type.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_airplane_type_unauthorized(self):
        payload = {
            "name": "New name",
        }
        res = self.client.post(AIRPLANE_TYPE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_airplane_type_unauthorized(self):
        payload = {
            "name": "Updated name",
        }

        url = detail_url(self.airplane_type.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_airplane_type_unauthorized(self):
        url = detail_url(self.airplane_type.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

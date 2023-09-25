from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Airport
from airport.tests.data_base import DataTestCase

AIRPORT_URL = reverse("airport:airport-list")


def detail_url(airport_id):
    return reverse("airport:airport-detail", args=[airport_id])


class AdminAirportApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AdminAirportApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_airport_list(self):
        res = self.client.get(AIRPORT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(self.airports), len(res.data))

    def test_get_airport_detail(self):
        url = detail_url(self.airport.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.airport.name)
        self.assertEqual(res.data["closets_big_city"], self.airport.closets_big_city)

    def test_post_airport(self):
        payload = {
            "name": "Crested airport",
            "closets_big_city": "Crested City",
        }

        res = self.client.post(AIRPORT_URL, payload)
        airport = Airport.objects.get(name=res.data["name"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(airport, key))

    def test_put_airport(self):
        payload = {
            "name": "Updated city",
            "closets_big_city": "Updated closets city",
        }

        url = detail_url(self.airport.pk)
        res = self.client.put(url, payload)
        airport = Airport.objects.get(name=res.data["name"])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(self.airports), len(res.data))
        self.assertIn(airport, self.airports)
        for key in payload:
            self.assertEqual(payload[key], getattr(airport, key))

    def test_delete_airport(self):
        url = detail_url(self.airport.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(res.data)


class AuthenticatedAirportApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AuthenticatedAirportApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="authenticated@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_airport_list(self):
        res = self.client.get(AIRPORT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(self.airports))

    def test_get_airport_detail(self):
        url = detail_url(self.airport.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.airport.name)
        self.assertEqual(res.data["closets_big_city"], self.airport.closets_big_city)

    def test_post_airport_forbidden(self):
        payload = {
            "name": "Created airport",
            "closets_big_city": "Crested City",
        }
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_airport_forbidden(self):
        payload = {
            "name": "Updated airport",
            "closets_big_city": "Updated City",
        }
        url = detail_url(self.airport.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_airport_forbidden(self):
        url = detail_url(self.airport.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class UnauthenticatedAirportApiTests(DataTestCase):
    def test_get_airport_list(self):
        res = self.client.get(AIRPORT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(self.airports))

    def test_get_airport_detail(self):
        url = detail_url(self.airport.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["name"], self.airport.name)
        self.assertEqual(res.data["closets_big_city"], self.airport.closets_big_city)

    def test_post_airport_unauthorized(self):
        payload = {
            "name": "Crested airport",
            "closets_big_city": "Crested City",
        }
        res = self.client.post(AIRPORT_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_airport_unauthorized(self):
        payload = {
            "name": "Crested airport",
            "closets_big_city": "Crested City",
        }
        url = detail_url(self.airport.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_airport_unauthorized(self):
        url = detail_url(self.airport.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

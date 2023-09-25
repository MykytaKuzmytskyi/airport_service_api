import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Flight
from airport.tests.data_base import DataTestCase

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id: int) -> str:
    return reverse("airport:flight-detail", args=[flight_id])


payload = {
    "route": 2,
    "airplane": 1,
    "departure_time": datetime.datetime.now(),
    "arrival_time": datetime.datetime.now(),
    "crew": [1, 2],
}


class AdminFlightApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AdminFlightApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_flight_list(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.flights), len(res.data))

    def test_get_flight_detail(self):
        url = detail_url(self.flight.pk)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["route"], str(self.flight.route))

    def test_post_flight(self):
        res = self.client.post(FLIGHT_URL, payload)
        flight = Flight.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(flight, self.flights)

    def test_put_flight(self):
        url = detail_url(self.flight.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(payload["route"], res.data["route"])
        self.assertEqual(payload["airplane"], res.data["airplane"])

    def test_delete_flight(self):
        url = detail_url(self.flight.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(res.data)
        self.assertNotIn(self.flight, self.flights)


class AuthenticatedFlightApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AuthenticatedFlightApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="authenticated@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_flight_list(self):
        res = self.client.get(FLIGHT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.flights), len(res.data))

    def test_get_flight_detail(self):
        url = detail_url(self.flight.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["route"], str(self.flight.route))
        self.assertEqual(res.data["airplane"], str(self.flight.airplane))

    def test_post_flight_forbidden(self):
        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_flight_forbidden(self):
        url = detail_url(self.flight.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_flight_forbidden(self):
        url = detail_url(self.flight.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class UnauthenticatedFlightApiTests(DataTestCase):
    def test_get_flight_list(self):
        res = self.client.get(FLIGHT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.flights), len(res.data))

    def test_get_flight_detail(self):
        url = detail_url(self.flight.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["route"], str(self.flight.route))
        self.assertEqual(res.data["airplane"], str(self.flight.airplane))

    def test_post_flight_forbidden(self):
        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_flight_forbidden(self):
        url = detail_url(self.flight.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_flight_forbidden(self):
        url = detail_url(self.flight.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

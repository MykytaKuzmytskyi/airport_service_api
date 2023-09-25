from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Crew
from airport.tests.data_base import DataTestCase

CREW_URL = reverse("airport:crew-list")


def detail_url(crew_id):
    return reverse("airport:crew-detail", args=[crew_id])


class AdminCrewApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AdminCrewApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_crew_list(self):
        res = self.client.get(CREW_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(self.crews), len(res.data))

    def test_get_crew_detail(self):
        url = detail_url(self.crew.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["first_name"], self.crew.first_name)
        self.assertEqual(res.data["last_name"], self.crew.last_name)

    def test_post_crew(self):
        payload = {
            "first_name": "Test first_name",
            "last_name": "Test last_name",
        }

        res = self.client.post(CREW_URL, payload)
        crew = Crew.objects.get(first_name=res.data["first_name"])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            self.assertEqual(payload[key], getattr(crew, key))

    def test_put_crew(self):
        payload = {
            "first_name": "Updated first_name",
            "last_name": "Updated last_name",
        }

        url = detail_url(self.crew.pk)
        res = self.client.put(url, payload)
        crew = Crew.objects.get(first_name=res.data["first_name"])

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(self.crews), len(res.data))
        self.assertIn(crew, self.crews)
        for key in payload:
            self.assertEqual(payload[key], getattr(crew, key))

    def test_delete_crew(self):
        url = detail_url(self.crew.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(res.data)


class AuthenticatedCrewApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AuthenticatedCrewApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="authenticated@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_crew_list_forbidden(self):
        res = self.client.get(CREW_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_crew_detail_forbidden(self):
        url = detail_url(self.crew.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_crew_forbidden(self):
        payload = {
            "first_name": "New first_name",
        }
        res = self.client.post(CREW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_crew_forbidden(self):
        payload = {
            "first_name": "Updated first_name",
        }
        url = detail_url(self.crew.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_crew_forbidden(self):
        url = detail_url(self.crew.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class UnauthenticatedCrewApiTests(DataTestCase):
    def test_get_crew_list_unauthorized(self):
        res = self.client.get(CREW_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_crew_detail_unauthorized(self):
        url = detail_url(self.crew.pk)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_crew_unauthorized(self):
        payload = {
            "first_name": "New first_name",
        }
        res = self.client.post(CREW_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_crew_unauthorized(self):
        payload = {
            "first_name": "Updated first_name",
        }
        url = detail_url(self.crew.pk)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_crew_unauthorized(self):
        url = detail_url(self.crew.pk)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

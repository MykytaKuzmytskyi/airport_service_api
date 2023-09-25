from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Route
from airport.serializers import RouteListSerializer
from airport.tests.data_base import DataTestCase

ROUTER_URL = reverse("airport:route-list")


def detail_url(route_id: int) -> str:
    return reverse("airport:route-detail", args=[route_id])


class AdminRouteApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AdminRouteApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_route_list(self):
        res = self.client.get(ROUTER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.routers), len(res.data))

    def test_get_route_detail(self):
        url = detail_url(1)
        res = self.client.get(url)
        route = Route.objects.get(id=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["source"], route.source.closets_big_city)

    def test_post_route(self):
        payload = {
            "source": 1,
            "destination": 3,
            "distance": 500,
        }
        res = self.client.post(ROUTER_URL, payload)
        route = Route.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(route, self.routers)

    def test_put_route(self):
        payload = {
            "source": 3,
            "destination": 1,
            "distance": 500,
        }
        url = detail_url(self.route1.id)
        # print(self.route.pk)
        # print(self.route.distance)
        res = self.client.put(url, payload)
        route = Route.objects.get(
            source=res.data["source"], destination=res.data["destination"]
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in payload:
            self.assertEqual(payload[key], res.data[key])
        # print(route.pk)
        # print(res.data["id"])
        # print(self.route.pk)
        # print(self.route.distance)
        # # self.assertEqual(payload["source"], self.route.source.pk)

    def test_delete_route(self):
        url = detail_url(self.route1.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(res.data)
        self.assertNotIn(self.route1, self.routers)


class AuthenticatedRouteApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AuthenticatedRouteApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="authenticated@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

    def test_get_route_list(self):
        res = self.client.get(ROUTER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.routers), len(res.data))

    def test_get_route_detail(self):
        url = detail_url(1)
        res = self.client.get(url)
        route = Route.objects.get(id=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["source"], route.source.closets_big_city)

    def test_post_route_forbidden(self):
        payload = {
            "source": 1,
            "destination": 3,
            "distance": 500,
        }
        res = self.client.post(ROUTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_route_forbidden(self):
        payload = {
            "source": 3,
            "destination": 1,
            "distance": 500,
        }
        url = detail_url(self.route1.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_route_forbidden(self):
        url = detail_url(self.route1.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_route_by_source(self):
        res = self.client.get(ROUTER_URL, {"source": f"{self.route1.source.name}"})
        serializer1 = RouteListSerializer(self.route1)
        serializer2 = RouteListSerializer(self.route2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)


class UnauthenticatedRouteApiTests(DataTestCase):
    def test_get_route_list(self):
        res = self.client.get(ROUTER_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.routers), len(res.data))

    def test_get_route_detail(self):
        url = detail_url(1)
        res = self.client.get(url)
        route = Route.objects.get(id=1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["source"], route.source.closets_big_city)

    def test_post_route_forbidden(self):
        payload = {
            "source": 1,
            "destination": 3,
            "distance": 500,
        }
        res = self.client.post(ROUTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_route_forbidden(self):
        payload = {
            "source": 3,
            "destination": 1,
            "distance": 500,
        }
        url = detail_url(self.route1.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_route_forbidden(self):
        url = detail_url(self.route1.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

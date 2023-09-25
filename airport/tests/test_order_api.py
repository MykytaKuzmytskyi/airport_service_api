from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Order, Ticket
from airport.tests.data_base import DataTestCase

ORDER_URL = reverse("airport:order-list")


class AdminAirportApiTests(DataTestCase):
    def setUp(self) -> None:
        super(AdminAirportApiTests, self).setUp()
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            email="admin@user.com",
            password="test12345",
        )
        self.client.force_authenticate(self.user)

        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            flight=self.flight, row=1, seat=2, order=self.order
        )
        Ticket.objects.create(flight=self.flight, row=1, seat=3, order=self.order)
        Ticket.objects.create(flight=self.flight, row=1, seat=4, order=self.order)
        self.tickets = Ticket.objects.all()

    def test_get_order_list(self):
        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(len(res.data[0]["tickets"]), 3)

    def test_create_tickets_in_order(self):
        payload = {"tickets": [
            {"row": 3, "seat": 3, "flight": 1},
            {"row": 3, "seat": 4, "flight": 1},
        ]}

        res = self.client.post(ORDER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(self.tickets), 5)

    def test_create_ticket_bad_request(self):
        payload = {"tickets": [
            {"row": 2, "seat": 25, "flight": 1},
        ]}
        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.exception, True)

    def test_validator_tickets(self):
        payload = {"tickets": [
            {"row": 1, "seat": 3, "flight": 1},
        ]}
        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.exception, True)
        # print(res.data['tickets'][0]['non_field_errors'][0])

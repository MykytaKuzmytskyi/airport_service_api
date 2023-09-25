from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Route,
    Crew,
    Flight,
    Ticket,
    Order,
)


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
        )


class AirplaneListSerializer(AirplaneSerializer):
    airplane_type = serializers.CharField(
        max_length=255,
        source="airplane_type.name",
        read_only=True,
    )

    class Meta:
        model = Airplane
        fields = (
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
        )


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(max_length=255, source="source.closets_big_city")
    destination = serializers.CharField(
        max_length=255, source="destination.closets_big_city"
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )


class RouteDetailSerializer(RouteSerializer):
    source = serializers.CharField(max_length=255, source="source.closets_big_city")
    destination = serializers.CharField(
        max_length=255, source="destination.closets_big_city"
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
        )


class FlightListSerializer(FlightSerializer):
    route = serializers.CharField(source="route.__str__")
    airplane = serializers.CharField(source="airplane.__str__")
    crew = CrewSerializer(many=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
        )


class TicketListSerializer(TicketSerializer):
    flight = FlightSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(), fields=["row", "seat"]
            )
        ]


class TicketCreateSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketCreateSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"], attrs["seat"], attrs["flight"].airplane, ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "flight",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Ticket.objects.all(), fields=["row", "seat"]
            )
        ]


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightDetailSerializer(FlightSerializer):
    route = serializers.StringRelatedField(many=False)
    airplane = serializers.StringRelatedField(many=False)
    crew = serializers.StringRelatedField(many=True)
    tickets_taken = TicketSeatsSerializer(
        source="tickets",
        many=True,
        read_only=True,
    )

    class Meta:
        model = Flight
        fields = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "tickets_taken",
        )


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketCreateSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "tickets",
        )

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "tickets",
        )

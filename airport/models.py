from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closets_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        to=AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self):
        return self.name + " " + self.airplane_type.name


class Route(models.Model):
    source = models.ForeignKey(
        to=Airport, on_delete=models.CASCADE, related_name="sources"
    )
    destination = models.ForeignKey(
        to=Airport, on_delete=models.CASCADE, related_name="destinations"
    )
    distance = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.source.closets_big_city} - {self.destination.closets_big_city}: {self.distance} km"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order: {self.user}"


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Flight(models.Model):
    route = models.ForeignKey(
        to=Route, on_delete=models.CASCADE, related_name="flights"
    )
    airplane = models.ForeignKey(
        to=Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(to=Crew)

    def __str__(self):
        return (
            f"From {self.route.source.closets_big_city} to {self.route.destination.closets_big_city}: "
            f"{self.departure_time.strftime('%m.%d.%Y, %H:%M')} - {self.arrival_time.strftime('%m.%d.%Y, %H:%M')}"
        )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        to=Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE, related_name="tickets")

    def __str__(self):
        return f"{str(self.flight)} (row: {self.row}, seat: {self.seat})"

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {airplane_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        self.full_clean()
        super(Ticket, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        unique_together = ("flight", "row", "seat")
        ordering = ["row", "seat"]

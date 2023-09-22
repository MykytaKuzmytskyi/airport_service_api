from django.conf import settings
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
        return f"Order: {self.user.username}"


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
            f"{self.departure_time} - {self.arrival_time}"
        )


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(
        to=Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")

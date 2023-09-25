import datetime

from airport.models import Airport, Route, AirplaneType, Airplane, Crew, Flight
from django.test import TestCase


class DataTestCase(TestCase):
    def setUp(self) -> None:
        airport_1 = Airport.objects.create(
            name="Boryspol Airport",
            closets_big_city="Boryspol",
        )
        airport_2 = Airport.objects.create(
            name="Lviv Airport",
            closets_big_city="Lviv",
        )
        airport_3 = Airport.objects.create(
            name="Charcov Airport",
            closets_big_city="Charcov",
        )
        route1 = Route.objects.create(
            source=airport_1,
            destination=airport_2,
            distance=650,
        )
        route2 = Route.objects.create(
            source=airport_2,
            destination=airport_3,
            distance=500,
        )
        airport_type = AirplaneType.objects.create(name="Airbus")
        AirplaneType.objects.create(name="Boing")
        AirplaneType.objects.create(name="Tu")
        airplane1 = Airplane.objects.create(
            name="A",
            rows=10,
            seats_in_row=10,
            airplane_type=airport_type,
        )
        Airplane.objects.create(
            name="B",
            rows=10,
            seats_in_row=10,
            airplane_type=airport_type,
        )
        Airplane.objects.create(
            name="C",
            rows=10,
            seats_in_row=10,
            airplane_type=airport_type,
        )
        crew1 = Crew.objects.create(first_name="First", last_name="First")
        crew2 = Crew.objects.create(first_name="Second", last_name="Second")
        Crew.objects.create(first_name="Third", last_name="Third")
        flight1 = Flight.objects.create(
            route=route1,
            airplane=airplane1,
            departure_time=datetime.datetime.now(),
            arrival_time=datetime.datetime.now(),
        )
        flight2 = Flight.objects.create(
            route=route2,
            airplane=airplane1,
            departure_time=datetime.datetime.now(),
            arrival_time=datetime.datetime.now(),
        )

        flight1.save()
        flight2.save()
        flight1.crew.add(crew1, crew2)
        flight2.crew.add(crew1, crew2)

        self.airports = Airport.objects.all()
        self.routers = Route.objects.all()
        self.airplane_types = AirplaneType.objects.all()
        self.airplanes = Airplane.objects.all()
        self.crews = Crew.objects.all()
        self.flights = Flight.objects.all()

        self.airport = Airport.objects.get(id=1)
        self.route1 = Route.objects.get(id=1)
        self.route2 = Route.objects.get(id=2)
        self.airplane_type = AirplaneType.objects.get(id=1)
        self.airplane = Airplane.objects.get(id=1)
        self.crew = Crew.objects.get(id=1)
        self.flight = Flight.objects.get(id=1)

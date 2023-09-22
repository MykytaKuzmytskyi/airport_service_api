from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from airport.models import Airport, AirplaneType, Airplane, Route
from airport.serializers import AirportSerializer, AirplaneTypeSerializer, AirplaneSerializer, AirplaneListSerializer, \
    RouteListSerializer, RouteDetailSerializer, RouteSerializer


class AirportViewSet(ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class AirplaneTypeViewSet(ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = [IsAdminUser]


class AirplaneViewSet(ModelViewSet):
    queryset = Airplane.objects.all()
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related("airplane_type")
        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer


class RouteViewSet(ModelViewSet):
    queryset = Route.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer

        if self.action == "retrieve":
            return RouteDetailSerializer

        return RouteSerializer

    def get_queryset(self):
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related("source", "destination")
        return queryset

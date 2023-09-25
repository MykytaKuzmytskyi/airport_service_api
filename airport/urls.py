from rest_framework import routers

from airport.views import (
    AirportViewSet,
    AirplaneTypeViewSet,
    AirplaneViewSet,
    RouteViewSet,
    CrewViewSet,
    FlightViewSet,
    OrderViewSet,
)

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)

urlpatterns = router.urls

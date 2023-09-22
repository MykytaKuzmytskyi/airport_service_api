from rest_framework import routers

from airport.views import (
    AirportViewSet, AirplaneTypeViewSet, AirplaneViewSet, RouteViewSet,
)

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("routes", RouteViewSet)

urlpatterns = router.urls

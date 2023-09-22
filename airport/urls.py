from rest_framework import routers

from airport.views import (
    AirportViewSet, AirplaneTypeViewSet, AirplaneViewSet, RouteViewSet, CrewViewSet,
)

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("routes", RouteViewSet)
router.register("crews", CrewViewSet)

urlpatterns = router.urls

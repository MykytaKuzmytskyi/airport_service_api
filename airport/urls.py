from rest_framework import routers

from airport.views import (
    AirportViewSet, AirplaneTypeViewSet,
)

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)
router.register("airplane_types", AirplaneTypeViewSet)


urlpatterns = router.urls

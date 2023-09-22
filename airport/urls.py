from rest_framework import routers

from airport.views import (
    AirportViewSet,
)

app_name = "airport"

router = routers.DefaultRouter()
router.register("airports", AirportViewSet)


urlpatterns = router.urls

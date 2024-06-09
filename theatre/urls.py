from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    ActorViewSet,
    GenreViewSet,
    PlayViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()
router.register("actors", ActorViewSet, basename="actors")
router.register("genres", GenreViewSet, basename="genres")
router.register("plays", PlayViewSet, basename="plays")
router.register("theatre_halls", TheatreHallViewSet, basename="theatre_halls")
router.register("performances", PerformanceViewSet, basename="performances")
router.register("tickets", TicketViewSet, basename="tickets")


urlpatterns = [path("", include(router.urls))]

app_name = "theatre"

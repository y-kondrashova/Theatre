from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, extend_schema_view

from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Ticket,
    Reservation,
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlaySerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    TheatreHallSerializer,
    TheatreHallListSerializer,
    TheatreHallDetailSerializer,
    PerformanceSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    TicketSerializer,
)


@extend_schema_view(
    list=extend_schema(summary="List of all actors"),
    retrieve=extend_schema(summary="Retrieve an actor by ID"),
    create=extend_schema(summary="Create new actor"),
    update=extend_schema(summary="Update existing actor"),
    partial_update=extend_schema(summary="Partially update existing actor"),
    destroy=extend_schema(summary="Delete an actor"),
)
class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


@extend_schema_view(
    list=extend_schema(summary="List of all genres"),
    retrieve=extend_schema(summary="Retrieve a genre by ID"),
    create=extend_schema(summary="Create new genre"),
    update=extend_schema(summary="Update existing genre"),
    partial_update=extend_schema(summary="Partially update existing genre"),
    destroy=extend_schema(summary="Delete a genre"),
)
class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


@extend_schema_view(
    list=extend_schema(summary="List of all plays"),
    retrieve=extend_schema(summary="Retrieve a play by ID"),
    create=extend_schema(summary="Create new play"),
    update=extend_schema(summary="Update existing play"),
    partial_update=extend_schema(summary="Partially update existing play"),
    destroy=extend_schema(summary="Delete a play"),
)
class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.prefetch_related("actors", "genres")
    serializer_class = PlaySerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        if self.action == "retrieve":
            return PlayDetailSerializer

        return self.serializer_class


@extend_schema_view(
    list=extend_schema(summary="List of all theatre halls"),
    retrieve=extend_schema(summary="Retrieve a theatre hall by ID"),
    create=extend_schema(summary="Create new theatre hall"),
    update=extend_schema(summary="Update existing theatre hall"),
    partial_update=extend_schema(
        summary="Partially update existing theatre hall"
    ),
    destroy=extend_schema(summary="Delete a theatre hall"),
)
class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TheatreHallListSerializer
        if self.action == "retrieve":
            return TheatreHallDetailSerializer
        return self.serializer_class


@extend_schema_view(
    list=extend_schema(summary="List of all performances"),
    retrieve=extend_schema(summary="Retrieve a performance by ID"),
    create=extend_schema(summary="Create new performance"),
    update=extend_schema(summary="Update existing performance"),
    partial_update=extend_schema(
        summary="Partially update existing performance"
    ),
    destroy=extend_schema(summary="Delete a performance"),
)
class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("play", "theatre_hall")
    serializer_class = PerformanceSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer
        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return self.serializer_class


@extend_schema_view(
    list=extend_schema(summary="List of all tickets"),
    retrieve=extend_schema(summary="Retrieve a ticket by ID"),
    create=extend_schema(summary="Create new ticket"),
    update=extend_schema(summary="Update existing ticket"),
    partial_update=extend_schema(summary="Partially update existing ticket"),
    destroy=extend_schema(summary="Delete a ticket"),
)
class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return (
            Ticket.objects
            .select_related("performance__play", "reservation")
            .filter(reservation__user=user)
        )

    def perform_create(self, serializer):
        user = self.request.user
        reservation = Reservation.objects.create(user=user)
        serializer.save(reservation=reservation)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

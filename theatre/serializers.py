from django.contrib.auth import get_user_model
from rest_framework import serializers

from theatre.models import (
    Actor,
    Genre,
    Play,
    TheatreHall,
    Performance,
    Reservation,
    Ticket,
)

User = get_user_model()


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


class PlayListSerializer(serializers.ModelSerializer):
    actors = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    genres = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )

    class Meta:
        model = Play
        fields = ["id", "title", "actors", "genres"]


class PlayDetailSerializer(PlaySerializer):
    actors = ActorSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = "__all__"


class TheatreHallListSerializer(TheatreHallSerializer):
    class Meta:
        model = TheatreHall
        fields = ["id", "name", "capacity"]


class TheatreHallDetailSerializer(TheatreHallSerializer):
    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_row", "capacity"]


class PerformanceSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time", "available_seats"]

    def get_available_seats(self, performance):
        total_seats = performance.theatre_hall.capacity
        reserved_seats = Ticket.objects.filter(
            performance_id=performance.id
        ).count()
        available_seats = total_seats - reserved_seats
        return available_seats


class PerformanceListSerializer(PerformanceSerializer):
    play = serializers.SlugRelatedField(read_only=True, slug_field="title")
    theatre_hall_name = serializers.CharField(
        read_only=True,
        source="theatre_hall.name",
    )
    theatre_hall_capacity = serializers.IntegerField(
        read_only=True, source="theatre_hall.capacity"
    )

    class Meta:
        model = Performance
        fields = [
            "id",
            "play",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "show_time",
            "available_seats",
        ]


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(read_only=True)
    theatre_hall = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
    )


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance"]

    def create(self, validated_data):
        reservation = validated_data.pop("reservation", None)
        user = self.context["request"].user
        if not reservation:
            reservation = Reservation.objects.create(user=user)
        ticket = Ticket.objects.create(
            reservation=reservation, **validated_data
        )
        return ticket

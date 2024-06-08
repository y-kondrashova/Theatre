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


class PlayListSerializer(PlaySerializer):
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

    class Meta:
        model = Play
        fields = ["id", "title", "description", "actors", "genres"]


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
    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]


class PerformanceListSerializer(PerformanceSerializer):
    play = serializers.SlugRelatedField(
        read_only=True, slug_field="title"
    )
    theatre_hall = serializers.SlugRelatedField(
        read_only=True, slug_field="name",
    )


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(read_only=True)
    theatre_hall = serializers.SlugRelatedField(
        read_only=True, slug_field="name",
    )


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user"]


class TicketSerializer(serializers.ModelSerializer):
    reservation = ReservationSerializer()

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance", "reservation"]

    def create(self, validated_data):
        reservation_data = validated_data.pop("reservation")
        reservation = Reservation.objects.create(**reservation_data)
        ticket = Ticket.objects.create(
            reservation=reservation, **validated_data
        )
        return ticket

    def update(self, instance, validated_data):
        reservation_data = validated_data.pop("reservation")
        reservation = Reservation.objects.create(**reservation_data)

        instance.row = validated_data.get("row", instance.row)
        instance.seat = validated_data.get("seat", instance.seat)
        instance.performance = validated_data.get(
            "performance", instance.performance
        )
        instance.reservation = reservation
        instance.save()

        return instance

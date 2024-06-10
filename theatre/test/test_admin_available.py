from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from theatre.models import Actor, Genre, TheatreHall, Play


class UserCannotCreateTest(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.genre = Genre.objects.create(name="Test Genre")
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_row=15
        )
        self.play = Play.objects.create(
            title="Test Play", description="Test Description"
        )
        self.play.actors.set([self.actor])
        self.play.genres.set([self.genre])

        self.client = APIClient()
        self.client.login(username="user", password="secretpass")

    def test_user_create_genre(self):
        self.client.credentials()
        data = {"name": "Test Genre"}

        response = self.client.post(
            reverse("theatre:genres-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_actor(self):
        self.client.credentials()
        data = {
            "first_name": "John",
            "last_name": "Doe",
        }

        response = self.client.post(
            reverse("theatre:actors-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_theatre_hall(self):
        self.client.credentials()
        data = {
            "name": "Test Hall",
            "rows": 10,
            "seats_in_row": 15
        }

        response = self.client.post(
            reverse("theatre:theatre_halls-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_play(self):
        self.client.credentials()
        data = {
            "title": "Test Play",
            "description": "Test Description",
            "actors": [self.actor.id],
            "genres": [self.genre.id],
        }

        response = self.client.post(
            reverse("theatre:plays-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create_performance(self):
        self.client.credentials()
        data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2024-06-23T17:00:00Z"
        }

        response = self.client.post(
            reverse("theatre:performances-list"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
from django.test import TestCase
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

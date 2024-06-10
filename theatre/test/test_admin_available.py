from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from theatre.test.samples import (
    sample_actor,
    sample_genre,
    sample_theatre_hall,
    sample_play,
    sample_user,
)


class BaseTestCase(TestCase):
    def setUp(self):
        self.actor = sample_actor()
        self.genre = sample_genre()
        self.theatre_hall = sample_theatre_hall()
        self.play = sample_play()
        self.play.actors.set([self.actor])
        self.play.genres.set([self.genre])
        self.client = APIClient()

    def create_entity(self, url, data, expected_status):
        response = self.client.post(reverse(url), data, format="json")
        self.assertEqual(response.status_code, expected_status)
        return response


class UserCannotCreateTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = sample_user(is_superuser=False)
        self.client.force_authenticate(user=self.user)

    def test_user_create_genre(self):
        self.client.credentials()
        data = {"name": "Test Genre"}
        self.create_entity(
            "theatre:genres-list", data, status.HTTP_403_FORBIDDEN
        )

    def test_user_create_actor(self):
        self.client.credentials()
        data = {
            "first_name": "John",
            "last_name": "Doe",
        }
        self.create_entity(
            "theatre:actors-list", data, status.HTTP_403_FORBIDDEN
        )

    def test_user_create_theatre_hall(self):
        self.client.credentials()
        data = {
            "name": "Test Hall",
            "rows": 10,
            "seats_in_row": 15
        }
        self.create_entity(
            "theatre:theatre_halls-list", data, status.HTTP_403_FORBIDDEN
        )

    def test_user_create_play(self):
        self.client.credentials()
        data = {
            "title": "Test Play",
            "description": "Test Description",
            "actors": [self.actor.id],
            "genres": [self.genre.id],
        }
        self.create_entity(
            "theatre:plays-list", data, status.HTTP_403_FORBIDDEN
        )

    def test_user_create_performance(self):
        self.client.credentials()
        data = {
            "play": self.play.id,
            "theatre_hall": self.theatre_hall.id,
            "show_time": "2024-06-23T17:00:00Z"
        }
        self.create_entity(
            "theatre:performances-list", data, status.HTTP_403_FORBIDDEN
        )


class AdminCanCreateTest(BaseTestCase):

    def setUp(self):
        super().setUp()

        self.admin_user = sample_user(is_superuser=True)
        self.client.force_authenticate(user=self.admin_user)

    def test_admin_create_actor(self):
        self.client.credentials()
        data = {"first_name": "John", "last_name": "Doe"}
        self.create_entity(
            "theatre:actors-list", data, status.HTTP_201_CREATED
        )

    def test_admin_create_genre(self):
        self.client.credentials()
        data = {"name": "Test Genre"}
        self.create_entity(
            "theatre:genres-list", data, status.HTTP_201_CREATED
        )

    def test_admin_create_play(self):
        self.client.credentials()
        data = {
            "title": "Test Play",
            "description": "Test Description",
            "actors": [self.actor.id],
            "genres": [self.genre.id],
        }
        self.create_entity(
            "theatre:plays-list", data, status.HTTP_201_CREATED
        )

    def test_admin_create_theatre_hall(self):
        self.client.credentials()
        data = {
            "name": "Test Hall",
            "rows": 10,
            "seats_in_row": 15
        }
        self.create_entity(
            "theatre:theatre_halls-list", data, status.HTTP_201_CREATED
        )

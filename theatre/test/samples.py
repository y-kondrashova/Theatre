from theatre.models import Actor, Genre, TheatreHall, Play


def sample_actor(**params):
    defaults = {"first_name": "John", "last_name": "Doe"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_genre(**params):
    defaults = {"name": "Test Genre"}
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_theatre_hall(**params):
    defaults = {
        "name": "Test Hall",
        "rows": 10,
        "seats_in_row": 15
    }
    defaults.update(params)
    return TheatreHall.objects.create(**defaults)


def sample_play(**params):
    defaults = {
        "title": "Test Play",
        "description": "Test Description",
    }
    defaults.update(params)
    return Play.objects.create(**defaults)

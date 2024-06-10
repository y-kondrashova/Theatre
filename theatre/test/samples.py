from theatre.models import Actor, Genre


def sample_actor(**params):
    defaults = {"first_name": "John", "last_name": "Doe"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


def sample_genre(**params):
    defaults = {"name": "Test Genre"}
    defaults.update(params)

    return Genre.objects.create(**defaults)
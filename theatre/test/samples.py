from theatre.models import Actor


def sample_actor(**params):
    defaults = {"first_name": "John", "last_name": "Doe"}
    defaults.update(params)

    return Actor.objects.create(**defaults)

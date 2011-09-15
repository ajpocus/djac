from fixture_generator import fixture_generator
from django.contrib.auth.models import User

@fixture_generator(User)
def test_user():
    foobar = User.objects.create(username="foobar")


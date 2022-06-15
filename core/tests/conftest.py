import pytest

from pytest_factoryboy import register

from core.tests.factories import UserFactory, ExerciseLogFactory, ProfileFactory

register(UserFactory)
register(ProfileFactory)
register(ExerciseLogFactory)

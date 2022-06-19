import datetime

import factory
import pytz
from django.conf import settings
from django.contrib.auth import get_user_model
from factory.fuzzy import FuzzyInteger, FuzzyDecimal

from factory.django import DjangoModelFactory
from faker import Faker

from core.models import Profile, ExerciseLog

tzinfo = pytz.timezone(settings.TIME_ZONE)
UserModel = get_user_model()

fake = Faker("ja_jp")


class UserFactory(DjangoModelFactory):
    class Meta:
        model = UserModel

    email = fake.ascii_safe_email()
    password = fake.password()
    is_staff = False
    is_active = True


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    nickname = fake.name()
    user = factory.SubFactory(UserFactory)


class ExerciseLogFactory(DjangoModelFactory):
    class Meta:
        model = ExerciseLog

    user = factory.SubFactory(UserFactory)
    exercise_date = datetime.date(2022, 1, 1)
    set_weight = FuzzyDecimal(0.0, 999.9, 1)
    one_set = FuzzyInteger(0, 5)
    two_set = FuzzyInteger(0, 5)
    three_set = FuzzyInteger(0, 5)
    four_set = FuzzyInteger(0, 5)
    five_set = FuzzyInteger(0, 5)

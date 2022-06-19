from decimal import Decimal

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from core.constants import ExerciseSettings
from core.models import Profile, Exercise

client = APIClient()
fake = Faker()


@pytest.mark.django_db
def test_get_next_exercise_first(user_factory):
    """getのテスト まだ何も登録がない場合"""
    user = user_factory.create()
    client.force_authenticate(user)
    url = "/api/v1/next-exercise/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 3
    assert data[0]["name"] == ExerciseSettings.SQUAT["name"]
    assert data[1]["name"] == ExerciseSettings.BENCH_PRESS["name"]
    assert data[2]["name"] == ExerciseSettings.BARBELL_ROWING["name"]


@pytest.mark.django_db
def test_get_next_exercise_second(user_factory, exercise_log_factory):
    """getのテスト 前回のトレーニングタイプがAの場合"""
    user = user_factory.create()
    client.force_authenticate(user)

    profile = Profile.objects.get(user=user)
    profile.exercise_flag = True
    profile.save()

    url = "/api/v1/next-exercise/"
    response = client.get(url)
    profile = Profile.objects.get(user=user)
    assert response.status_code == status.HTTP_200_OK
    assert profile.exercise_flag
    data = response.data
    assert len(data) == 3
    assert data[0]["name"] == ExerciseSettings.SQUAT["name"]
    assert data[1]["name"] == ExerciseSettings.SHOULDER_PRESS["name"]
    assert data[2]["name"] == ExerciseSettings.DEAD_LIFT["name"]

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
def test_get_next_exercise_second(user_factory):
    """getのテスト 前回のトレーニングタイプがAの場合"""
    user = user_factory.create()
    client.force_authenticate(user)

    profile = Profile.objects.get(user=user)
    profile.exercise_flag = True
    profile.save()

    url = "/api/v1/next-exercise/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # DBから取得し直す
    profile.refresh_from_db()
    assert profile.exercise_flag
    data = response.data
    assert len(data) == 3
    assert data[0]["name"] == ExerciseSettings.SQUAT["name"]
    assert data[1]["name"] == ExerciseSettings.SHOULDER_PRESS["name"]
    assert data[2]["name"] == ExerciseSettings.DEAD_LIFT["name"]


@pytest.mark.django_db
def test_get_next_exercise_before_exercise_type_b(user_factory, exercise_log_factory):
    """getのテスト 前回のトレーニングタイプがBの場合"""
    user = user_factory.create()
    client.force_authenticate(user)

    exercise = Exercise.objects.filter(exercise_type__contains="B").all()

    _ = exercise_log_factory.create(user=user, exercise=exercise[0])
    _ = exercise_log_factory.create(user=user, exercise=exercise[1])
    _ = exercise_log_factory.create(user=user, exercise=exercise[2])

    profile = Profile.objects.get(user=user)

    url = "/api/v1/next-exercise/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # DBから取得し直す
    profile.refresh_from_db()
    assert not profile.exercise_flag
    data = response.data
    assert len(data) == 3
    assert data[0]["name"] == ExerciseSettings.SQUAT["name"]
    assert data[1]["name"] == ExerciseSettings.BENCH_PRESS["name"]
    assert data[2]["name"] == ExerciseSettings.BARBELL_ROWING["name"]


@pytest.mark.django_db
def test_get_next_exercise_before_exercise_set_weight_achieved_type_a(
    user_factory, exercise_log_factory
):
    """getのテスト 前回のトレーニングタイプAが目標達成している場合"""
    user = user_factory.create()
    client.force_authenticate(user)

    exercise = Exercise.objects.filter(exercise_type__contains="A").all()

    squat = exercise_log_factory.create(user=user, exercise=exercise[0])
    bench_press = exercise_log_factory.create(user=user, exercise=exercise[1])
    barbell_rowing = exercise_log_factory.create(user=user, exercise=exercise[2])

    # テストのため強制的にフラグをFalseにする
    profile = Profile.objects.get(user=user)
    profile.exercise_flag = False
    profile.save()

    url = "/api/v1/next-exercise/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 3
    assert data[0]["name"] == ExerciseSettings.SQUAT["name"]
    assert Decimal(data[0]["set_weight"]) == squat.set_weight + Decimal(2.5)
    assert data[1]["name"] == ExerciseSettings.BENCH_PRESS["name"]
    assert Decimal(data[1]["set_weight"]) == bench_press.set_weight + Decimal(2.5)
    assert data[2]["name"] == ExerciseSettings.BARBELL_ROWING["name"]
    assert Decimal(data[2]["set_weight"]) == barbell_rowing.set_weight + Decimal(2.5)


@pytest.mark.django_db
def test_get_next_exercise_before_exercise_not_set_weight_achieved_type_a(
    user_factory, exercise_log_factory
):
    """getのテスト 前回のトレーニングタイプAが目標達成していない場合"""
    user = user_factory.create()
    client.force_authenticate(user)

    exercise = Exercise.objects.filter(exercise_type__contains="A").all()

    squat = exercise_log_factory.create(user=user, exercise=exercise[0], five_set=3)
    bench_press = exercise_log_factory.create(
        user=user, exercise=exercise[1], five_set=3
    )
    barbell_rowing = exercise_log_factory.create(
        user=user, exercise=exercise[2], five_set=3
    )

    # テストのため強制的にフラグをFalseにする
    profile = Profile.objects.get(user=user)
    profile.exercise_flag = False
    profile.save()

    url = "/api/v1/next-exercise/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 3
    assert data[0]["name"] == ExerciseSettings.SQUAT["name"]
    assert Decimal(data[0]["set_weight"]) == squat.set_weight
    assert data[1]["name"] == ExerciseSettings.BENCH_PRESS["name"]
    assert Decimal(data[1]["set_weight"]) == bench_press.set_weight
    assert data[2]["name"] == ExerciseSettings.BARBELL_ROWING["name"]
    assert Decimal(data[2]["set_weight"]) == barbell_rowing.set_weight


@pytest.mark.django_db
def test_get_next_exercise_before_exercise_set_weight_achieved_type_b(
    user_factory, exercise_log_factory
):
    """getのテスト 前回のトレーニングタイプBが目標達成している場合"""
    user = user_factory.create()
    client.force_authenticate(user)

    exercise = Exercise.objects.filter(exercise_type__contains="B").all()

    squat = exercise_log_factory.create(user=user, exercise=exercise[0])
    shoulder_press = exercise_log_factory.create(user=user, exercise=exercise[1])
    dead_lift = exercise_log_factory.create(user=user, exercise=exercise[2])

    # テストのため強制的にフラグをFalseにする
    profile = Profile.objects.get(user=user)
    profile.exercise_flag = True
    profile.save()

    url = "/api/v1/next-exercise/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 3
    assert data[0]["name"] == ExerciseSettings.SQUAT["name"]
    assert Decimal(data[0]["set_weight"]) == squat.set_weight + Decimal(2.5)
    assert data[1]["name"] == ExerciseSettings.SHOULDER_PRESS["name"]
    assert Decimal(data[1]["set_weight"]) == shoulder_press.set_weight + Decimal(2.5)
    assert data[2]["name"] == ExerciseSettings.DEAD_LIFT["name"]
    assert Decimal(data[2]["set_weight"]) == dead_lift.set_weight + Decimal(5.0)


@pytest.mark.django_db
def test_get_next_exercise_before_exercise_not_set_weight_achieved_type_b(
    user_factory, exercise_log_factory
):
    """getのテスト 前回のトレーニングタイプBが目標達成していない場合"""
    user = user_factory.create()
    client.force_authenticate(user)

    exercise = Exercise.objects.filter(exercise_type__contains="B").all()

    squat = exercise_log_factory.create(user=user, exercise=exercise[0], five_set=3)
    shoulder_press = exercise_log_factory.create(
        user=user, exercise=exercise[1], five_set=3
    )
    dead_lift = exercise_log_factory.create(
        user=user,
        exercise=exercise[2],
        one_set=1,
        two_set=1,
        three_set=1,
        four_set=1,
        five_set=0,
    )

    # テストのため強制的にフラグをFalseにする
    profile = Profile.objects.get(user=user)
    profile.exercise_flag = True
    profile.save()

    url = "/api/v1/next-exercise/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert len(data) == 3
    assert data[0]["name"] == ExerciseSettings.SQUAT["name"]
    assert Decimal(data[0]["set_weight"]) == squat.set_weight
    assert data[1]["name"] == ExerciseSettings.SHOULDER_PRESS["name"]
    assert Decimal(data[1]["set_weight"]) == shoulder_press.set_weight
    assert data[2]["name"] == ExerciseSettings.DEAD_LIFT["name"]
    assert Decimal(data[2]["set_weight"]) == dead_lift.set_weight

import datetime
from decimal import Decimal

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from core.constants import ExerciseSettings
from core.models import ExerciseLog, Exercise

client = APIClient()
fake = Faker()

base_url = "/api/v1/exercise-log/"
exercise_date = datetime.date(2022, 1, 1)


@pytest.mark.django_db
def test_get_exercise_log_all(user_factory, exercise_log_factory):
    """getのテスト(全件）"""
    user = user_factory.create()
    exercise_squat = Exercise.objects.get(code=ExerciseSettings.SQUAT["code"])
    _ = exercise_log_factory.create(
        user=user,
        exercise=exercise_squat,
    )
    client.force_authenticate(user)
    url = base_url
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_exercise_log(user_factory, exercise_log_factory):
    """getのテスト（1件）"""
    user = user_factory.create()
    exercise_squat = Exercise.objects.get(code=ExerciseSettings.SQUAT["code"])
    exercise_log = exercise_log_factory.create(
        user=user,
        exercise=exercise_squat,
    )
    client.force_authenticate(user)
    url = f"{base_url}{exercise_log.id}/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_post_exercise_log(user_factory):
    """postのテスト"""
    user = user_factory.create()
    client.force_authenticate(user)
    exercise_squat = Exercise.objects.get(code=ExerciseSettings.SQUAT["code"])
    url = base_url
    params = {
        "exercise": exercise_squat.id,
        "exercise_date": exercise_date,
        "set_weight": Decimal(20),
        "one_set": 5,
        "two_set": 5,
        "three_set": 5,
        "four_set": 5,
        "five_set": 5,
    }
    response = client.post(url, params, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    # リクエスト通り反映されているか確認
    data = response.data
    assert data["user"] == user.id
    assert data["exercise"] == exercise_squat.id
    assert data["exercise_date"] == exercise_date.strftime("%Y-%m-%d")
    assert Decimal(data["set_weight"]) == Decimal(params["set_weight"])
    assert data["one_set"] == params["one_set"]
    assert data["two_set"] == params["two_set"]
    assert data["three_set"] == params["three_set"]
    assert data["four_set"] == params["four_set"]
    assert data["five_set"] == params["five_set"]


@pytest.mark.django_db
def test_post_exercise_log_over_register(user_factory, exercise_log_factory):
    """postのテスト 既に同じ日に3種目のトレーニングが登録されている場合"""
    user = user_factory.create()
    client.force_authenticate(user)
    exercise_type_a = Exercise.objects.filter(
        code__in=[
            ExerciseSettings.SQUAT["code"],
            ExerciseSettings.BENCH_PRESS["code"],
            ExerciseSettings.BARBELL_ROWING["code"],
        ]
    )
    _ = exercise_log_factory.create(
        user=user, exercise=exercise_type_a[0], exercise_date=exercise_date
    )
    _ = exercise_log_factory.create(
        user=user, exercise=exercise_type_a[1], exercise_date=exercise_date
    )
    _ = exercise_log_factory.create(
        user=user, exercise=exercise_type_a[2], exercise_date=exercise_date
    )
    url = base_url
    params = {
        "exercise": exercise_type_a[0].id,
        "exercise_date": exercise_date,
        "set_weight": Decimal(20),
        "one_set": 5,
        "two_set": 5,
        "three_set": 5,
        "four_set": 5,
        "five_set": 5,
    }
    response = client.post(url, params, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_post_exercise_log_duplicate_same_exercise(user_factory, exercise_log_factory):
    """postのテスト 同じ日に同じ種目を複数登録するのは不可"""
    user = user_factory.create()
    client.force_authenticate(user)
    exercise_squat = Exercise.objects.get(code=ExerciseSettings.SQUAT["code"])
    _ = exercise_log_factory.create(user=user, exercise=exercise_squat)
    url = f"/api/v1/exercise-log/"
    params = {
        "exercise": exercise_squat.id,
        "exercise_date": exercise_date,
        "set_weight": Decimal(20),
        "one_set": 5,
        "two_set": 5,
        "three_set": 5,
        "four_set": 5,
        "five_set": 5,
    }
    response = client.post(url, params, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_post_exercise_log_consecutive_days(user_factory, exercise_log_factory):
    """postのテスト 連日のトレーニング登録は不可（トレーニング種目は問わず）"""
    user = user_factory.create()
    client.force_authenticate(user)
    exercise_squat = Exercise.objects.get(code=ExerciseSettings.SQUAT["code"])
    _ = exercise_log_factory.create(user=user, exercise=exercise_squat)
    url = f"/api/v1/exercise-log/"
    params = {
        "exercise": exercise_squat.id,
        "exercise_date": exercise_date + datetime.timedelta(days=1),
        "set_weight": Decimal(20),
        "one_set": 5,
        "two_set": 5,
        "three_set": 5,
        "four_set": 5,
        "five_set": 5,
    }
    response = client.post(url, params, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_put_exercise_log_view(user_factory, exercise_log_factory):
    """putのテスト"""
    user = user_factory.create()
    client.force_authenticate(user)
    exercise_squat = Exercise.objects.get(code=ExerciseSettings.SQUAT["code"])
    exercise_log = exercise_log_factory.create(
        user=user, exercise=exercise_squat, exercise_date=exercise_date
    )
    url = f"{base_url}{exercise_log.id}/"
    response = client.put(
        url,
        {
            "id": exercise_log.id,
            "exercise": exercise_squat.id,
            "exercise_date": exercise_date + datetime.timedelta(days=1),
            "set_weight": Decimal(20),
            "one_set": 5,
            "two_set": 5,
            "three_set": 5,
            "four_set": 5,
            "five_set": 5,
        },
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_patch_exercise_log_view(user_factory, exercise_log_factory):
    """patchのテスト"""
    user = user_factory.create()
    client.force_authenticate(user)
    exercise_squat = Exercise.objects.get(code=ExerciseSettings.SQUAT["code"])
    exercise_log = exercise_log_factory.create(
        user=user, exercise=exercise_squat, exercise_date=exercise_date
    )
    url = f"{base_url}{exercise_log.id}/"
    response = client.patch(
        url,
        {"exercise_date": exercise_date + datetime.timedelta(days=1)},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_delete_exercise_log_view(user_factory, exercise_log_factory):
    """deleteのテスト"""
    user = user_factory.create()
    client.force_authenticate(user)
    exercise_type_a = Exercise.objects.filter(
        code__in=[
            ExerciseSettings.SQUAT["code"],
            ExerciseSettings.BENCH_PRESS["code"],
            ExerciseSettings.BARBELL_ROWING["code"],
        ]
    )
    exercise_log1 = exercise_log_factory.create(
        user=user, exercise=exercise_type_a[0], exercise_date=exercise_date
    )
    exercise_log2 = exercise_log_factory.create(
        user=user, exercise=exercise_type_a[1], exercise_date=exercise_date
    )
    url = f"{base_url}{exercise_log1.id}/"
    response = client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT

    exercise_log1_after = ExerciseLog.objects.filter(id=exercise_log1.id)
    assert not exercise_log1_after

    exercise_log2_after = ExerciseLog.objects.filter(id=exercise_log2.id)
    assert exercise_log2_after

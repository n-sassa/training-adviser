import datetime

import pytest
from faker import Faker

from core.models import ExerciseLog, Exercise

fake = Faker("ja_jp")


@pytest.mark.django_db
def test_is_empty():
    """トレーニング記録 初期状態では何も登録されていないことをチェック"""
    saved_exercise_logs = ExerciseLog.objects.all()
    assert saved_exercise_logs.count() == 0


@pytest.mark.django_db
def test_is_created(exercise_log_factory):
    exercise_all = Exercise.objects.all()

    exercise_log = exercise_log_factory.create(
        exercise=exercise_all[0], exercise_date=datetime.date(2022, 1, 1)
    )
    print(exercise_log)
    assert True

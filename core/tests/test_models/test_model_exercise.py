import pytest
from faker import Faker

from core.constants import ExerciseSettings
from core.models import Exercise

fake = Faker("ja_jp")


@pytest.mark.django_db
def test_row_count():
    """トレーニング種目 初期状態で種目が5つ登録されているか確認"""
    exercise_all = Exercise.objects.all()
    assert exercise_all.count() == 5


@pytest.mark.django_db
def test_check_exercise_details():
    """トレーニング種目の内容が正しく登録されているか確認"""
    exercise_all = Exercise.objects.order_by("code").values()

    for setting in ExerciseSettings.EXERCISE_SETTINGS_LIST:
        exercise = next(
            (
                exercise
                for exercise in exercise_all
                if exercise["code"] == setting["code"]
            ),
            None,
        )
        assert exercise, f"トレーニング種目" + setting["name"] + "が登録されていません。"
        assert exercise["name"] == setting["name"], "登録されているトレーニング種目が誤っています。"
        assert (
            exercise["exercise_type"] == setting["exercise_type"]
        ), "登録されているタイプが誤っています。"
        assert (
            exercise["default_rep"] == setting["default_rep"]
        ), "登録されている1セット毎の回数が誤っています。"

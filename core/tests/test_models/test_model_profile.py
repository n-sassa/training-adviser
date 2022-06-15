import datetime

import pytest
from django.db.models import Q
from faker import Faker

from core.models import Profile, Exercise

fake = Faker("ja_jp")


@pytest.mark.django_db
def test_check_created_profile(user_factory):
    """ユーザーモデル作成時にプロフィールが自動で作られているか確認"""
    user1 = user_factory.create(email=fake.ascii_safe_email())
    user2 = user_factory.create(email=fake.ascii_safe_email())
    user3 = user_factory.create(email=fake.ascii_safe_email())
    profile_all = Profile.objects.values()

    for user in [user1, user2, user3]:
        target_profile = [
            profile for profile in profile_all if profile["user_id"] == user.id
        ]
        assert len(target_profile) == 1, "1ユーザに1プロフィールにならなければいけません。"


@pytest.mark.django_db
def test_change_exercise_flag(user_factory, exercise_log_factory):
    """エクササイズログ(エクササイズタイプAorB）が作成されたらフラグが変わるか確認"""
    # ユーザー作成
    user = user_factory.create()
    # プロフィールのフラグを確認
    profile = Profile.objects.get(user=user)
    # データ作成直後の状態を確認
    assert profile.exercise_flag == False

    # トレーニング種目のexercise_typeがAのものを取得
    exercises_type_a = Exercise.objects.filter(
        Q(exercise_type="A") | Q(exercise_type="AB")
    )

    exercise_date = datetime.date(2022, 1, 1)

    for exercise in exercises_type_a:
        exercise_log_factory.create(
            user=user, exercise=exercise, exercise_date=exercise_date
        )

    # DBからデータを取得し直す
    profile.refresh_from_db()
    assert profile.exercise_flag == True

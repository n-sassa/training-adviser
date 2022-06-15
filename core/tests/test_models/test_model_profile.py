import pytest
from faker import Faker

from core.models import Profile

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

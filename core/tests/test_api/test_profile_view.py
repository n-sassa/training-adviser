import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Profile

client = APIClient()
fake = Faker()


@pytest.mark.django_db
def test_get_profile(user_factory):
    """getのテスト 新規作成後
    ・新規作成後に自身のプロフィールを取得できる
    ・nicknameとexercise_flagがデフォルト値になっている
    """
    user = user_factory.create()
    client.force_authenticate(user)
    profile = Profile.objects.get(user=user)
    url = f"/api/v1/profile/{profile.id}/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = response.data
    assert data["nickname"] == "名無し"
    assert data["user"] == user.id
    assert data["exercise_flag"] == False


@pytest.mark.django_db
def test_get_profile_only_me(user_factory):
    """getのテスト 自分のユーザのプロフィールのみ確認できる"""
    user1 = user_factory.create()
    user2 = user_factory.create(email=fake.ascii_safe_email(), password=fake.password())

    client.force_authenticate(user1)
    url = f"/api/v1/profile/"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

    user2_profile = Profile.objects.get(user=user2)
    url_user2 = f"{url}{user2_profile.id}/"
    response = client.get(url_user2)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    client.force_authenticate(user2)
    response = client.get(url_user2)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_put_profile_view(user_factory):
    """putのテスト"""
    user = user_factory.create()
    client.force_authenticate(user)
    profile = Profile.objects.get(user=user)
    url = f"/api/v1/profile/{profile.id}/"
    nickname = "test"
    response = client.put(
        url,
        {"id": str(user.id), "nickname": nickname},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.data["nickname"] == nickname


# 以下許可していないアクセスの確認
def test_post_profile_view():
    """postのテスト"""
    response = client.post("/api/v1/profile/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_delete_profile_view():
    """deleteのテスト"""
    response = client.delete("/api/v1/profile/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patch_profile_view():
    """patchのテスト"""
    response = client.patch(f"/api/v1/profile/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

import pytest
from faker import Faker
from rest_framework import status
from rest_framework.test import APIClient

from core.models import User

client = APIClient()
fake = Faker()


@pytest.mark.django_db
def test_post_create_user_view():
    """postのテスト"""
    email = fake.ascii_safe_email()
    password = fake.password()

    response = client.post(
        "/api/v1/create/",
        {"email": email, "password": password},
    )
    assert response.status_code == status.HTTP_201_CREATED

    user = User.objects.get(email=email)
    assert user, "ユーザーが作成されていません"
    # ハッシュ化されているので一致しない
    assert user.password != password, "パスワードがハッシュ化されていません"


# 以下許可していないアクセスの確認
def test_get_create_user_view():
    """getのテスト"""
    response = client.get("/api/v1/create/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_put_create_user_view():
    """putのテスト"""
    response = client.put("/api/v1/create/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_delete_create_user_view():
    """deleteのテスト"""
    response = client.delete("/api/v1/create/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


def test_patch_create_user_view():
    """patchのテスト"""
    response = client.patch(f"/api/v1/create/")
    assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

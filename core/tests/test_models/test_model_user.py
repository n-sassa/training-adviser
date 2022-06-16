import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from faker import Faker

from core.models import Profile, Exercise

fake = Faker("ja_jp")


@pytest.mark.django_db
def test_create_user(user_factory):
    """ユーザーモデルの作成"""
    email = fake.ascii_safe_email()
    password = fake.password()
    user = get_user_model().objects.create_user(email=email, password=password)
    assert user.email == email
    assert user.password != password  # ハッシュ化されるので一致しない
    assert user.is_active == True
    assert user.is_staff == False
    assert user.is_superuser == False


@pytest.mark.django_db
def test_create_user_with_no_email(user_factory):
    """emailがNoneの場合"""
    password = fake.password()
    with pytest.raises(ValueError) as e:
        _ = get_user_model().objects.create_user(email=None, password=password)
    assert str(e.value) == "Emailは必須です"


@pytest.mark.django_db
def test_create_user_with_duplicate(user_factory):
    """emailが既に使われている場合"""
    email = fake.ascii_safe_email()
    password = fake.password()
    # 登録済みユーザー作成
    _ = get_user_model().objects.create_user(email=email, password=password)
    # 同じemailで登録
    with pytest.raises(IntegrityError, match=r"UNIQUE constraint*"):
        _ = get_user_model().objects.create_user(email=email, password=password)


@pytest.mark.django_db
def test_create_superuser(user_factory):
    """スーパーユーザーの作成"""
    email = fake.ascii_safe_email()
    password = fake.password()
    user = get_user_model().objects.create_superuser(email=email, password=password)
    assert user.email == email
    assert user.password != password  # ハッシュ化されるので一致しない
    assert user.is_active == True
    assert user.is_staff == True
    assert user.is_superuser == True


@pytest.mark.django_db
def test_create_superuser(user_factory):
    """スーパーユーザーの作成 emailがNoneの場合"""
    password = fake.password()
    with pytest.raises(ValueError) as e:
        _ = get_user_model().objects.create_superuser(email=None, password=password)
    assert str(e.value) == "Emailは必須です"


@pytest.mark.django_db
def test_create_superuser_with_duplicate(user_factory):
    """スーパーユーザーの作成 emailが既に使われている場合"""
    email = fake.ascii_safe_email()
    password = fake.password()
    # 登録済みユーザー作成
    _ = get_user_model().objects.create_superuser(email=email, password=password)
    # 同じemailで登録
    with pytest.raises(IntegrityError, match=r"UNIQUE constraint*"):
        _ = get_user_model().objects.create_superuser(email=email, password=password)

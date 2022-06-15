from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import ulid

from utils.customfield import ULIDField


class BaseModel(models.Model):
    """ベースモデル
    共通項目を設定しておき継承して使う
    """

    id = ULIDField(default=ulid.new, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserManager(BaseUserManager):
    """カスタムユーザーマネージャ
    Django標準ではusernameとpasswordで認証するところを
    emailとpasswordで認証できるようにする
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Emailは必須です")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザモデル
    django標準はusernameでユーザ登録するが
    emailで登録するようカスタム
    """

    id = ULIDField(default=ulid.new, primary_key=True, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Profile(BaseModel):
    """プロフィール"""

    nickname = models.CharField(max_length=20, null=True, blank=False, default="名無し")
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    exercise_flag = models.BooleanField(default=False)

    class Meta:
        db_table = "profile"

    def __str__(self):
        return self.nickname


class Exercise(BaseModel):
    """トレーニング種目"""

    EXERCISE_TYPE_CHOICES = (("A", "SetA"), ("B", "SetB"), ("AB", "Always"))

    DEFAULT_REP_CHOICES = (("1", "1rep / 1set"), ("5", "5rep / 1set"))

    code = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=50)
    exercise_type = models.CharField(max_length=2, choices=EXERCISE_TYPE_CHOICES)
    default_rep = models.CharField(max_length=2, choices=DEFAULT_REP_CHOICES)

    class Meta:
        db_table = "exercise"

    def __str__(self):
        return self.name


class ExerciseLog(BaseModel):
    """トレーニング記録"""

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    exercise_date = models.DateField()
    set_weight = models.DecimalField(default=0, max_digits=4, decimal_places=1)
    one_set = models.PositiveSmallIntegerField(default=0)
    two_set = models.PositiveSmallIntegerField(default=0)
    three_set = models.PositiveSmallIntegerField(default=0)
    four_set = models.PositiveSmallIntegerField(default=0)
    five_set = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = "exercise_log"

    def __str__(self):
        return f"{self.user}: {self.set_weight}"

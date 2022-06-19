from decimal import Decimal

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .constants import ExerciseSettings
from .models import ExerciseLog, Profile, Exercise


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "password", "id")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        return user


class ProfileSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = Profile
        fields = ["id", "nickname", "user", "exercise_flag", "created_at", "updated_at"]
        extra_kwargs = {
            "user": {"read_only": True},
            "exercise_flag": {"read_only": True},
        }


class ExerciseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)

    class Meta:
        model = Exercise
        fields = [
            "id",
            "name",
            "exercise_type",
            "default_rep",
            "created_at",
            "updated_at",
        ]


class ExerciseLogSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M:%S", read_only=True)
    exercise_name = serializers.SerializerMethodField()

    class Meta:
        model = ExerciseLog
        fields = [
            "id",
            "user",
            "exercise",
            "exercise_name",
            "exercise_date",
            "set_weight",
            "one_set",
            "two_set",
            "three_set",
            "four_set",
            "five_set",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {"user": {"read_only": True}}

    def get_exercise_name(self, instance):
        return instance.exercise.name


class NextExerciseSerializer(serializers.ModelSerializer):
    set_weight = serializers.SerializerMethodField()

    def get_set_weight(self, instance):
        """トレーニング結果を元に次回のトレーニングウエイトを出力

        大条件: default_repを5セットできた場合
        　小条件1: default_repが5の場合 (デッドリフト以外)
        　  -> 今回のトレーニングウエイト + 2.5kgのウエイトを出力
          小条件2: default_repが1の場合 (デッドリフト)
            -> 今回のトレーニングウエイト + 5kgのウエイトを出力

        　未達成 -> 今回のトレーニングウエイトと同じウエイトを出力

        """
        exercise_log_list: list[ExerciseLog] = instance.exercise_log

        # トレーニング履歴がない場合は一般的なスタートの重さを返す
        if not exercise_log_list:
            if instance.code == ExerciseSettings.DEAD_LIFT["code"]:
                return "40.0"
            return "20.0"

        recent_exercise_date = exercise_log_list[0].exercise_date

        recent_exercise_log = ExerciseLog.objects.filter(
            exercise_date=recent_exercise_date
        )
        if len(recent_exercise_log) <= 3:
            return str(exercise_log_list[0].set_weight)

        sets = [
            exercise_log_list[0].one_set,
            exercise_log_list[0].two_set,
            exercise_log_list[0].three_set,
            exercise_log_list[0].four_set,
            exercise_log_list[0].five_set,
        ]
        default_rep = int(exercise_log_list[0].exercise.default_rep)
        sets_average = sum(sets) / default_rep

        if sets_average >= default_rep:
            if default_rep == 5:
                return str(exercise_log_list[0].set_weight + Decimal(2.5))
            return str(exercise_log_list[0].set_weight + Decimal(5))

        return str(exercise_log_list[0].set_weight)

    class Meta:
        model = Exercise
        fields = ["id", "name", "set_weight"]

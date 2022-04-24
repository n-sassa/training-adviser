from decimal import Decimal

from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    ExerciseLog,
    Profile,
    Exercise
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'id')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)

        return user


class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S', read_only=True)
    updated_on = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'user', 'exercise_flag', 'created_on', 'updated_on']
        extra_kwargs = {'user': {'read_only': True}}



class ExerciseSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S', read_only=True)
    updated_on = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S', read_only=True)

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'exercise_type', 'default_rep', 'created_on', 'updated_on']


class ExerciseLogSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S', read_only=True)
    updated_on = serializers.DateTimeField(format='%Y/%m/%d %H:%M:%S', read_only=True)
    next_set_weight = serializers.SerializerMethodField()

    class Meta:
        model = ExerciseLog
        fields = [
            'id',
            'user',
            'exercise',
            'exercise_date',
            'set_weight',
            'one_set',
            'two_set',
            'three_set',
            'four_set',
            'five_set',
            'next_set_weight',
            'created_on',
            'updated_on'
        ]
        extra_kwargs = {'user': {'read_only': True}}

    def get_next_set_weight(self, obj):
        ''' トレーニング結果を元に次回のトレーニングウエイトを出力

        大条件: default_repを5セットできた場合
        　小条件1: default_repが5の場合 (デッドリフト以外)
        　  -> 今回のトレーニングウエイト + 2.5kgのウエイトを出力
          小条件2: default_repが1の場合 (デッドリフト)
            -> 今回のトレーニングウエイト + 5kgのウエイトを出力

        　未達成 -> 今回のトレーニングウエイトと同じウエイトを出力

        '''
        sets = [
            obj.one_set,
            obj.two_set,
            obj.three_set,
            obj.four_set,
            obj.five_set
        ]
        default_rep = int(obj.exercise.default_rep)
        sets_average = sum(sets) / default_rep

        if sets_average >= default_rep:
            if default_rep == 5:
                return str(obj.set_weight + Decimal(2.5))
            return str(obj.set_weight + Decimal(5))

        return str(obj.set_weight)


class NextExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = ['id',]

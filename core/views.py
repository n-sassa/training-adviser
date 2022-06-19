import datetime
from copy import deepcopy
from typing import Union

from django.db.models import OuterRef, Prefetch
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.date_util import str_to_date
from .constants import ResMsg
from .serializers import (
    UserSerializer,
    ProfileSerializer,
    ExerciseSerializer,
    ExerciseLogSerializer,
    NextExerciseSerializer,
)
from .models import Profile, Exercise, ExerciseLog


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        response = {"message": "POST method is not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        response = {"message": "DELETE method is not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        response = {"message": "PATCH method is not allowed"}
        return Response(response, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (AllowAny,)


class ExerciseLogViewSet(viewsets.ModelViewSet):
    queryset = ExerciseLog.objects.select_related("exercise").all()
    serializer_class = ExerciseLogSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data

        # オーバーワークだった場合は登録不可
        is_over_work, response_detail = self.check_over_work(
            request.user.id, data["exercise"], data["exercise_date"]
        )
        if is_over_work:
            return Response(**response_detail)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @classmethod
    def check_over_work(
        cls, user_id: str, exercise_id: str, exercise_date: str
    ) -> (bool, Union[dict, None]):
        """オーバーワークの判定
        オーバーワークの場合はresponseの内容も返す

        Args:
            user_id: str
            exercise_id: str
            exercise_date: str

        Returns:
            (bool, Union[dict, None])
        """
        # オーバーワークと判定された場合の共通response内容
        fail_response_detail = deepcopy(ResMsg.OVERWORK)

        # トレーニングの登録は1日3種目までのため登録しようとしている日付のものと前回のデータが取れれば良いためlimitを6とする
        exercise_log = (
            ExerciseLog.objects.select_related("exercise")
            .filter(
                user_id=user_id,
            )
            .order_by("-exercise_date")
            .all()[:6]
        )

        # exercise_dateをdatetime.date型に変換
        exercise_date = str_to_date(exercise_date)

        # 登録しようとしているデータのexercise_dateと同日のトレーニング記録を取得
        target_log = [log for log in exercise_log if log.exercise_date == exercise_date]

        # 一日に三種目以上の登録はオーバーワーク
        if len(target_log) >= 3:
            fail_response_detail["data"]["advice"] = "一日に3種目まで。"
            return True, fail_response_detail

        # 一日に同じ種目の登録はオーバーワーク
        if any(log for log in target_log if str(log.exercise_id) == exercise_id):
            fail_response_detail["data"]["advice"] = "同じトレーニングは同日に設定できません。"
            return True, fail_response_detail

        # 連日のトレーニングはオーバーワーク
        one_days_ago = exercise_date - datetime.timedelta(days=1)
        one_days_ago_log = [
            log for log in exercise_log if log.exercise_date == one_days_ago
        ]
        if one_days_ago_log:
            fail_response_detail["data"]["advice"] = "最低限1日休みましょう。"
            return True, fail_response_detail

        # オーバーワークではない
        return False, None


class NextExerciseView(APIView):
    def get(self, request):
        profile = Profile.objects.only("exercise_flag").get(user=request.user)
        exercises = Exercise.objects.prefetch_related(
            Prefetch(
                "exerciselog_set",
                queryset=ExerciseLog.objects.filter(user=request.user).order_by(
                    "-exercise_date"
                ),
                to_attr="exercise_log",
            )
        )

        if not profile.exercise_flag:
            next_exercise = exercises.filter(exercise_type__contains="A")
        else:
            next_exercise = exercises.filter(exercise_type__contains="B")

        serializer = NextExerciseSerializer(next_exercise, many=True)

        return Response(serializer.data)

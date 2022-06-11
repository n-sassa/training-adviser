from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExerciseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = (AllowAny,)


class ExerciseLogViewSet(viewsets.ModelViewSet):
    queryset = ExerciseLog.objects.all()
    serializer_class = ExerciseLogSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NextExerciseView(APIView):
    def get(self, request):
        exercise_flag = (
            Profile.objects.filter(user=request.user)
            .values("exercise_flag")
            .first()
            .get("exercise_flag")
        )
        exercises = Exercise.objects.all()

        if not exercise_flag:
            next_exercise = exercises.filter(exercise_type__contains="A")
        else:
            next_exercise = exercises.filter(exercise_type__contains="B")

        serializer = NextExerciseSerializer(next_exercise, many=True)

        return Response(serializer.data)

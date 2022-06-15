from .constants import ExerciseSettings
from .models import Exercise, ExerciseLog, Profile


def create_default_exercises(sender, **kwargs):
    Exercise.objects.get_or_create(**ExerciseSettings.SQUAT)
    Exercise.objects.get_or_create(**ExerciseSettings.BENCH_PRESS)
    Exercise.objects.get_or_create(**ExerciseSettings.BARBELL_ROWING)
    Exercise.objects.get_or_create(**ExerciseSettings.SHOULDER_PRESS)
    Exercise.objects.get_or_create(**ExerciseSettings.DEAD_LIFT)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


def change_exercise_flag(sender, instance, created, **kwargs):
    if created:
        exercise_date = instance.exercise_date
        queryset_count = (
            ExerciseLog.objects.select_related("user")
            .filter(user=instance.user, exercise_date=exercise_date)
            .count()
        )

        if queryset_count == 3:
            user_profile = Profile.objects.get(user=instance.user)
            user_profile.exercise_flag = not user_profile.exercise_flag
            user_profile.save()

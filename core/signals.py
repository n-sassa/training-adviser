from django.db.models import Q

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
        exercise_log = (
            ExerciseLog.objects.select_related("exercise")
            .filter(
                user=instance.user,
                exercise_date=exercise_date,
            )
            .values_list("exercise__exercise_type")
        )

        # トレーニングタイプがA かつ 3種目登録されたらトレーニングフラグをTrueにする
        exercise_type_a = [x for x in exercise_log if "A" in x[0]]

        if len(exercise_type_a) == 3:
            user_profile = Profile.objects.get(user=instance.user)
            user_profile.exercise_flag = True
            user_profile.save()
            return

        # トレーニングタイプがB かつ ３種目登録されたらトレーニングフラグをFalseにする
        exercise_type_b = [x for x in exercise_log if "B" in x[0]]

        if len(exercise_type_b) == 3:
            user_profile = Profile.objects.get(user=instance.user)
            user_profile.exercise_flag = False
            user_profile.save()
            return
        return

from .models import Exercise, ExerciseLog, Profile


def create_default_exercises(sender, **kwargs):
    Exercise.objects.get_or_create(name="スクワット", exercise_type="AB", default_rep=5)
    Exercise.objects.get_or_create(name="ベンチプレス", exercise_type="A", default_rep=5)
    Exercise.objects.get_or_create(name="バーベルロウ", exercise_type="A", default_rep=5)
    Exercise.objects.get_or_create(name="ショルダープレス", exercise_type="B", default_rep=5)
    Exercise.objects.get_or_create(name="デッドリフト", exercise_type="B", default_rep=1)


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
            user_profile = Profile.objects.filter(user=instance.user).first()
            user_profile.exercise_flag = not user_profile.exercise_flag
            user_profile.save()

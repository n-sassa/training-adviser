from django.apps import AppConfig
from django.db.models.signals import post_migrate, post_save


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        from core.signals import (
            create_default_exercises,
            create_user_profile,
            change_exercise_flag,
        )
        from .models import User, ExerciseLog

        post_migrate.connect(create_default_exercises, sender=self)
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(change_exercise_flag, sender=ExerciseLog)

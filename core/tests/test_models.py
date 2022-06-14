from django.test import TestCase

from core.models import Profile, Exercise, ExerciseLog


class ProfileModelTests(TestCase):
    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""
        saved_profiles = Profile.objects.all()
        self.assertEqual(saved_profiles.count(), 0)


class ExerciseModelTests(TestCase):
    def test_check_initial(self):
        """初期状態で種目が5つ登録されているか確認"""
        saved_exercises = Exercise.objects.all()
        self.assertEqual(saved_exercises.count(), 5)


class ExerciseLogModelTests(TestCase):
    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""
        saved_exercise_logs = ExerciseLog.objects.all()
        self.assertEqual(saved_exercise_logs.count(), 0)

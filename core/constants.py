class ExerciseSettings:
    SQUAT = {
        "code": 1,
        "name": "スクワット",
        "exercise_type": "AB",
        "default_rep": "5",
    }
    BENCH_PRESS = {
        "code": 2,
        "name": "ベンチプレス",
        "exercise_type": "A",
        "default_rep": "5",
    }
    BARBELL_ROWING = {
        "code": 3,
        "name": "バーベルロウ",
        "exercise_type": "A",
        "default_rep": "5",
    }
    SHOULDER_PRESS = {
        "code": 4,
        "name": "ショルダープレス",
        "exercise_type": "B",
        "default_rep": "5",
    }
    DEAD_LIFT = {
        "code": 5,
        "name": "デッドリフト",
        "exercise_type": "B",
        "default_rep": "1",
    }

    EXERCISE_SETTINGS_LIST = [
        SQUAT,
        BENCH_PRESS,
        BARBELL_ROWING,
        SHOULDER_PRESS,
        DEAD_LIFT,
    ]

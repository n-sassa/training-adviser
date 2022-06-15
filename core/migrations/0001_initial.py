# Generated by Django 4.0.4 on 2022-06-15 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ulid.api.api
import utils.customfield


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', utils.customfield.ULIDField(default=ulid.api.api.Api.new, editable=False, max_length=26, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', utils.customfield.ULIDField(default=ulid.api.api.Api.new, editable=False, max_length=26, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('code', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=50)),
                ('exercise_type', models.CharField(choices=[('A', 'SetA'), ('B', 'SetB'), ('AB', 'Always')], max_length=2)),
                ('default_rep', models.CharField(choices=[('1', '1rep / 1set'), ('5', '5rep / 1set')], max_length=2)),
            ],
            options={
                'db_table': 'exercise',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', utils.customfield.ULIDField(default=ulid.api.api.Api.new, editable=False, max_length=26, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('nickname', models.CharField(default='名無し', max_length=20, null=True)),
                ('exercise_flag', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'profile',
            },
        ),
        migrations.CreateModel(
            name='ExerciseLog',
            fields=[
                ('id', utils.customfield.ULIDField(default=ulid.api.api.Api.new, editable=False, max_length=26, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exercise_date', models.DateField()),
                ('set_weight', models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ('one_set', models.PositiveSmallIntegerField(default=0)),
                ('two_set', models.PositiveSmallIntegerField(default=0)),
                ('three_set', models.PositiveSmallIntegerField(default=0)),
                ('four_set', models.PositiveSmallIntegerField(default=0)),
                ('five_set', models.PositiveSmallIntegerField(default=0)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exercise_log',
            },
        ),
    ]

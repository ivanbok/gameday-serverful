# Generated by Django 4.0.5 on 2022-06-29 15:33

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('formatted_name', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='RaceResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_datetime', models.IntegerField()),
                ('position_1', models.CharField(blank=True, max_length=255)),
                ('position_2', models.CharField(blank=True, max_length=255)),
                ('position_3', models.CharField(blank=True, max_length=255)),
                ('position_4', models.CharField(blank=True, max_length=255)),
                ('position_5', models.CharField(blank=True, max_length=255)),
                ('position_6', models.CharField(blank=True, max_length=255)),
                ('position_7', models.CharField(blank=True, max_length=255)),
                ('position_8', models.CharField(blank=True, max_length=255)),
                ('position_9', models.CharField(blank=True, max_length=255)),
                ('position_10', models.CharField(blank=True, max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameday.country')),
            ],
        ),
        migrations.CreateModel(
            name='BetResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_datetime', models.IntegerField()),
                ('bet_amount', models.IntegerField()),
                ('winnings', models.IntegerField()),
                ('bet_type', models.CharField(blank=True, max_length=255)),
                ('bet_value', models.CharField(blank=True, max_length=255)),
                ('result_value', models.CharField(blank=True, max_length=255)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameday.country')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gameday.raceresult')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
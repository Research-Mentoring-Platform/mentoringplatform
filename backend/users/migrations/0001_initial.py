# Generated by Django 3.2.4 on 2021-06-13 14:41

from django.db import migrations, models
import users.methods
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('email', models.EmailField(max_length=48, unique=True, verbose_name='Email address')),
                ('username', models.CharField(max_length=16, unique=True, verbose_name='Username')),
                ('first_name', models.CharField(max_length=20, verbose_name='First name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Last name')),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('is_mentor', models.BooleanField(blank=True, default=False, verbose_name='Is mentor?')),
                ('is_mentee', models.BooleanField(blank=True, default=False, verbose_name='Is mentee?')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin?')),
                ('email_verified', models.BooleanField(default=False, verbose_name='Email verified?')),
                ('email_verification_token',
                 models.CharField(default=users.methods.generate_email_verification_token, max_length=32)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

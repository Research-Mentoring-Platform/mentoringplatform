# Generated by Django 3.2.4 on 2021-06-11 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MenteeDepartment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('label', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MenteeDesignation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('label', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='MenteeDiscipline',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('label', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Mentee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('about_self', models.TextField(blank=True, max_length=512)),
                ('profile_completed', models.BooleanField(default=False)),
                ('specialization', models.TextField(blank=True, max_length=256)),
                ('rating', models.DecimalField(decimal_places=2, max_digits=3, null=True)),
                ('department',
                 models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='departments',
                                   to='mentee.menteedepartment')),
                ('designation',
                 models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='designations',
                                   to='mentee.menteedesignation')),
                ('discipline',
                 models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='disciplines',
                                   to='mentee.menteediscipline')),
                (
                'user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

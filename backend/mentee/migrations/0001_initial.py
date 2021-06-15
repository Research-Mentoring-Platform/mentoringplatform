# Generated by Django 3.2.4 on 2021-06-15 18:17

import uuid

import django.db.models.expressions
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mentee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('about_self', models.TextField(blank=True, max_length=512)),
                ('profile_completed', models.BooleanField(default=False)),
                ('specialization', models.TextField(blank=True, max_length=256)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
            ],
        ),
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
            name='MenteeResearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=128)),
                ('organization', models.CharField(max_length=128)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('details', models.TextField(blank=True, max_length=512)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='researches',
                                             to='mentee.mentee')),
            ],
            options={
                'verbose_name_plural': 'MenteeResearches',
                'ordering': [
                    django.db.models.expressions.OrderBy(django.db.models.expressions.F('end_date'), descending=True,
                                                         nulls_last=False), '-start_date'],
            },
        ),
        migrations.CreateModel(
            name='MenteeEducation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('qualification', models.CharField(max_length=128)),
                ('organization', models.CharField(max_length=128)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('details', models.TextField(blank=True, max_length=512)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations',
                                             to='mentee.mentee')),
            ],
            options={
                'ordering': [
                    django.db.models.expressions.OrderBy(django.db.models.expressions.F('end_date'), descending=True,
                                                         nulls_last=False), '-start_date'],
            },
        ),
        migrations.AddField(
            model_name='mentee',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT,
                                    related_name='mentees_with_department', to='mentee.menteedepartment'),
        ),
        migrations.AddField(
            model_name='mentee',
            name='designation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT,
                                    related_name='mentees_with_designation', to='mentee.menteedesignation'),
        ),
        migrations.AddField(
            model_name='mentee',
            name='discipline',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT,
                                    related_name='mentees_with_discipline', to='mentee.menteediscipline'),
        ),
        migrations.AddField(
            model_name='mentee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

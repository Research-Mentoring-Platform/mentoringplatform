# Generated by Django 3.2.4 on 2021-06-11 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mentee', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mentor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=64)),
                ('agenda', models.CharField(blank=True, max_length=128)),
                ('date_time', models.DateTimeField()),
                ('url', models.URLField(blank=True)),
                ('creator',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings_created',
                                   to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mentorship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('start_date', models.DateField(verbose_name='Start date')),
                ('end_date', models.DateField(verbose_name='End date')),
                ('expected_end_date', models.DateField(blank=True, null=True, verbose_name='Expected end date')),
                ('mentee',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentee_mentorships',
                                   to='mentee.mentee')),
                ('mentor',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentor_mentorships',
                                   to='mentor.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='Research',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=128)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('organization', models.CharField(max_length=128)),
                ('details', models.TextField(blank=True, max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='researches',
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField(max_length=256)),
                ('mentorship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='milestones',
                                                 to='mentorship.mentorship')),
            ],
        ),
        migrations.CreateModel(
            name='MentorshipRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('statement_of_purpose', models.TextField(blank=True, max_length=512)),
                ('expectations', models.TextField(blank=True, max_length=256)),
                ('commitment', models.TextField(blank=True, max_length=256)),
                ('status', models.IntegerField(choices=[(1, 'Ongoing'), (2, 'Finished'), (3, 'Terminated')],
                                               default=(1, 'Ongoing'))),
                ('reject_reason', models.TextField(blank=True, max_length=256)),
                ('date', models.DateField(auto_now_add=True)),
                ('mentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentee.mentee')),
                ('mentor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mentor.mentor')),
            ],
        ),
        migrations.CreateModel(
            name='MeetingSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('description', models.TextField(blank=True, max_length=512)),
                ('todos', models.TextField(blank=True, max_length=512)),
                ('next_meeting_date', models.DateTimeField()),
                ('next_meeting_agenda', models.TextField(blank=True, max_length=512)),
                ('meeting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='summary',
                                                 to='mentorship.meeting')),
            ],
        ),
        migrations.AddField(
            model_name='meeting',
            name='mentorship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meetings',
                                    to='mentorship.mentorship'),
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('qualification', models.CharField(max_length=128)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
                ('organization', models.CharField(max_length=128)),
                ('details', models.TextField(blank=True, max_length=512)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='educations',
                                           to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

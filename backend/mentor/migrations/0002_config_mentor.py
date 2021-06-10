
from django.db import migrations

from config.update_db_using_configs import (
    add_mentor_designation,
    add_mentor_department,
    add_mentor_discipline,
    add_mentor_responsibility
)


class Migration(migrations.Migration):
    dependencies = [
        ('mentor', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_mentor_designation),
        migrations.RunPython(add_mentor_department),
        migrations.RunPython(add_mentor_discipline),
        migrations.RunPython(add_mentor_responsibility)
    ]

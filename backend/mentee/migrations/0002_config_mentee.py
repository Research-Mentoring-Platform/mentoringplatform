from django.db import migrations

from config.update_db_using_configs import (
    add_mentee_designation,
    add_mentee_department,
    add_mentee_discipline
)


class Migration(migrations.Migration):
    dependencies = [
        ('mentee', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_mentee_designation),
        migrations.RunPython(add_mentee_department),
        migrations.RunPython(add_mentee_discipline),
    ]
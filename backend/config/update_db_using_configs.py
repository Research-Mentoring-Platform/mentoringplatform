import json

PATH_CONFIG_DESIGNATION = 'config/designation.json'
PATH_CONFIG_DEPARTMENT = 'config/department.json'
PATH_CONFIG_DISCIPLINE = 'config/discipline.json'
PATH_CONFIG_MENTOR_RESPONSIBILITY = 'config/mentor_responsibility.json'


# TODO Add validation for the rows loaded using the config files
def add_mentor_designation(apps, schema_editor):
    with open(PATH_CONFIG_DESIGNATION, 'r') as f:
        config = json.load(f)

    model = apps.get_model('mentor', 'MentorDesignation')
    data = config['mentor']
    for label in data['values']:
        model.objects.create(label=label)


def add_mentee_designation(apps, schema_editor):
    with open(PATH_CONFIG_DESIGNATION, 'r') as f:
        config = json.load(f)

    model = apps.get_model('mentee', 'MenteeDesignation')
    data = config['mentor'] if config['mentee']['same_as_mentor'] else config['mentee']
    for label in data['values']:
        model.objects.create(label=label)


def add_mentor_department(apps, schema_editor):
    with open(PATH_CONFIG_DEPARTMENT, 'r') as f:
        config = json.load(f)

    model = apps.get_model('mentor', 'MentorDepartment')
    data = config['mentor']
    for label in data['values']:
        model.objects.create(label=label)


def add_mentee_department(apps, schema_editor):
    with open(PATH_CONFIG_DEPARTMENT, 'r') as f:
        config = json.load(f)

    model = apps.get_model('mentee', 'MenteeDepartment')
    data = config['mentor'] if config['mentee']['same_as_mentor'] else config['mentee']
    for label in data['values']:
        model.objects.create(label=label)


def add_mentor_discipline(apps, schema_editor):
    with open(PATH_CONFIG_DISCIPLINE, 'r') as f:
        config = json.load(f)

    model = apps.get_model('mentor', 'MentorDiscipline')
    data = config['mentor']
    for label in data['values']:
        model.objects.create(label=label)


def add_mentee_discipline(apps, schema_editor):
    with open(PATH_CONFIG_DISCIPLINE, 'r') as f:
        config = json.load(f)

    model = apps.get_model('mentee', 'MenteeDiscipline')
    data = config['mentor'] if config['mentee']['same_as_mentor'] else config['mentee']
    for label in data['values']:
        model.objects.create(label=label)


def add_mentor_responsibility(apps, schema_editor):
    with open(PATH_CONFIG_MENTOR_RESPONSIBILITY, 'r') as f:
        config = json.load(f)

    model = apps.get_model('mentor', 'MentorResponsibility')
    for description in config['values']:
        model.objects.create(description=description)


if __name__ == '__main__':
    pass

import json
import random

from django.contrib.auth.hashers import make_password

PATH_CONFIG_DESIGNATION = 'config/designation.json'
PATH_CONFIG_DEPARTMENT = 'config/department.json'
PATH_CONFIG_DISCIPLINE = 'config/discipline.json'
PATH_CONFIG_MENTOR_RESPONSIBILITY = 'config/mentor_responsibility.json'

# TODO remove this in production!
PATH_CONFIG_TEST_USER = 'config/test_users.json'


# TODO remove this in production!
def add_test_user(apps, schema_editor):
    # TODO unregister send-email signal
    with open(PATH_CONFIG_TEST_USER, 'r') as f:
        config = json.load(f)

    model = apps.get_model('users', 'CustomUser')

    mentor_model = apps.get_model('mentor', 'Mentor')
    mentor_responsibility = apps.get_model('mentor', 'MentorResponsibility')
    mentor_designation = apps.get_model('mentor', 'MentorDesignation')
    mentor_department = apps.get_model('mentor', 'MentorDepartment')
    mentor_discipline = apps.get_model('mentor', 'MentorDiscipline')

    mentee_model = apps.get_model('mentee', 'Mentee')
    mentee_designation = apps.get_model('mentee', 'MenteeDesignation')
    mentee_department = apps.get_model('mentee', 'MenteeDepartment')
    mentee_discipline = apps.get_model('mentee', 'MenteeDiscipline')

    for user_dict in config['users']:
        user = model.objects.create(**user_dict)
        user.password = make_password(user_dict['password'])
        user.email_verified = True
        user.save()
        if user.is_mentor:
            mentor = mentor_model.objects.create(user=user)
            mentor.profile_completed = True
            mentor.is_verified = True
            mentor.designation = random.choice(list(mentor_designation.objects.all()))
            mentor.department = random.choice(list(mentor_department.objects.all()))
            mentor.discipline = random.choice(list(mentor_discipline.objects.all()))
            mentor.specialization = 'Mentor {} {} specialization...'.format(user.first_name, user.last_name)
            mentor.responsibilities.set(random.sample(list(mentor_responsibility.objects.all()),
                                                      random.randint(1, mentor_responsibility.objects.all().count())))
            mentor.save()

        elif user.is_mentee:  # no profile for superuser
            mentee = mentee_model.objects.create(user=user)
            mentee.profile_completed = True
            mentee.designation = random.choice(list(mentee_designation.objects.all()))
            mentee.department = random.choice(list(mentee_department.objects.all()))
            mentee.discipline = random.choice(list(mentee_discipline.objects.all()))
            mentee.specialization = 'Mentee {} {} specialization...'.format(user.first_name, user.last_name)
            mentee.save()


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

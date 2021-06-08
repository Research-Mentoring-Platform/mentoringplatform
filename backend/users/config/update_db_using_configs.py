import json

PATH_CONFIG_DESIGNATION = 'designation.json'
PATH_CONFIG_DEPARTMENT = 'department.json'
PATH_CONFIG_DISCIPLINE = 'discipline.json'
PATH_CONFIG_MENTOR_RESPONSIBILITY = 'mentor_responsibility.json'


def fill_designations(apps):
    with open(PATH_CONFIG_DESIGNATION, 'r') as f:
        designations = json.load(f)

    model = apps.get_model('mentor', 'MentorDesignation')
    for label in designations['mentor']:
        model.create(label=label)

    model = apps.get_model('mentee', 'MenteeDesignation')
    for label in designations['mentee']:
        model.create(label=label)

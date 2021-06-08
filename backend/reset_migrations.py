import os
from glob import glob
from django.conf import settings


def reset():
    # https://stackoverflow.com/questions/15556499/django-db-settings-improperly-configured-error/46516080
    if getattr(settings, 'PRODUCTION_SERVER', False):
        print('This file should not be executed on the production server. Please use migrations/fixtures instead.')
        print('Exiting')
        return

    confirm = input('Are you sure you wish to continue? (y/n): ').lower()
    if confirm != 'y':
        print('Cancelling operation')
        return

    for file in glob('*/migrations/[!_]*.py'):
        print('Removing', file)
        os.remove(file)

    os.system('python manage.py makemigrations')
    print('Done')


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    reset()

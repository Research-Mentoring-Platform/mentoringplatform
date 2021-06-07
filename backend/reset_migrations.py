import os
from glob import glob
from django.conf import settings


def reset():
    if getattr(settings, 'PRODUCTION_SERVER', False):
        print('This file should not be executed on the production server. Please use migrations/fixtures instead.')
        print('Exiting...')
        return

    confirm = input('Are you sure to continue? (y/n): ').lower()
    if confirm == 'n':
        print('Cancelling operation')
        return

    for file in glob('*/migrations/000*.py'):
        print('removing', str(file))
        os.remove(file)

    os.system('python manage.py makemigrations')


if __name__ == '__main__':
    print('Must always run this from a Django console as follows:\n')
    file_name = os.path.basename(__file__).split('.')[0]
    print('python manage.py shell')
    print('>> import {}'.format(file_name))
    print('>> {}.reset()'.format(file_name))

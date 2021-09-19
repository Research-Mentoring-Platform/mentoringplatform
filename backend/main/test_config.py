from django.conf import settings
from django.test.runner import DiscoverRunner


class MyTestSuiteRunner(DiscoverRunner):

    def __init__(self, *args, **kwargs):
        super(MyTestSuiteRunner, self).__init__(*args, **kwargs)

    def setup_test_environment(self, **kwargs):
        super(MyTestSuiteRunner, self).setup_test_environment(debug=self.debug_mode)
        settings.EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'

#!/usr/bin/env python
import logging
from os.path import abspath, dirname, join
from shutil import rmtree
import sys

import django
from django.conf import settings

sys.path.insert(0, abspath(dirname(__file__)))

media_root = join(abspath(dirname(__file__)), 'test_files')
rmtree(media_root, ignore_errors=True)

installed_apps = [
    'simple_history.tests',
    'simple_history.tests.custom_user',
    'simple_history.tests.external',
    'simple_history.registry_tests.migration_test_app',

    'simple_history',

    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
]

DEFAULT_SETTINGS = dict(
    AUTH_USER_MODEL='custom_user.CustomUser',
    ROOT_URLCONF='simple_history.tests.urls',
    MEDIA_ROOT=media_root,
    STATIC_URL='/static/',
    INSTALLED_APPS=installed_apps,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    MIDDLEWARE_CLASSES=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    ],
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    }],
)


def main():

    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)
    if hasattr(django, 'setup'):
        django.setup()
    try:
        from django.test.runner import DiscoverRunner
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner
        failures = DjangoTestSuiteRunner(failfast=False).run_tests(['tests'])
        failures |= DjangoTestSuiteRunner(failfast=False).run_tests(['registry_tests'])
    else:
        failures = DiscoverRunner(failfast=False).run_tests(['simple_history.tests'])
        failures |= DiscoverRunner(failfast=False).run_tests(['simple_history.registry_tests'])
    sys.exit(failures)


if __name__ == "__main__":
    logging.basicConfig()
    main()

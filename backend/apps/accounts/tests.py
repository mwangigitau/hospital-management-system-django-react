import os
from io import StringIO
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from apps.accounts.models import Role


class AccountRoleAndCommandTests(TestCase):
    def test_signal_assigns_group_from_role(self):
        role = Role.objects.create(name='Nurse')
        user = get_user_model().objects.create_user(username='nurse1', password='test-pass', role=role)

        self.assertTrue(user.groups.filter(name='Nurse').exists())

    def test_createuser_command_creates_user_with_role(self):
        Role.objects.create(name='Doctor')
        stdout = StringIO()

        call_command(
            'createuser',
            username='doctor1',
            password='test-pass',
            email='doctor1@example.com',
            role='Doctor',
            stdout=stdout,
        )

        user = get_user_model().objects.get(username='doctor1')
        self.assertEqual(user.role.name, 'Doctor')
        self.assertTrue(user.groups.filter(name='Doctor').exists())

    def test_createsuperuser_command_creates_superuser(self):
        with mock.patch.dict(os.environ, {'DJANGO_SUPERUSER_PASSWORD': 'strong-pass-123'}):
            call_command(
                'createsuperuser',
                '--noinput',
                username='admin1',
                email='admin1@example.com',
            )

        user = get_user_model().objects.get(username='admin1')
        self.assertTrue(user.is_superuser)

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from apps.accounts.models import Role


class Command(BaseCommand):
    help = 'Create a regular HMS user.'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--password', required=True)
        parser.add_argument('--email', default='')
        parser.add_argument('--first-name', default='')
        parser.add_argument('--last-name', default='')
        parser.add_argument('--employee-id', default=None)
        parser.add_argument('--role', default=None, help='Role name')

    def handle(self, *args, **options):
        User = get_user_model()
        role = None
        if options['role']:
            role = Role.objects.filter(name=options['role']).first()
            if role is None:
                raise CommandError(f"Role '{options['role']}' does not exist.")

        user = User.objects.create_user(
            username=options['username'],
            password=options['password'],
            email=options['email'],
            first_name=options['first_name'],
            last_name=options['last_name'],
            employee_id=options['employee_id'],
            role=role,
        )
        self.stdout.write(self.style.SUCCESS(f"Created user '{user.username}'"))

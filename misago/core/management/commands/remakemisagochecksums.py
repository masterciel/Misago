from django.core.management.base import BaseCommand
from django.utils.encoding import force_str
from django.utils.six.moves import input

from ...signals import secret_key_changed


class Command(BaseCommand):
    help = 'Regenerates Misago checksums after SECRET_KEY changed.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            dest='force',
            default=False,
            help='Do not ask for confirmation',
        )

    def handle(self, *args, **options):
        message = force_str("This will replace all checksums "
                            "in database with new ones, marking "
                            "all data as trusted. Are you sure "
                            "you wish to continue? [Y/n]")
        if options['force'] or input(message).strip().lower() == "y":
            self.stdout.write("\nRegenerating checksums...")
            secret_key_changed.send(self)
            self.stdout.write("\nDone!")
        else:
            self.stdout.write("\nAborted!")

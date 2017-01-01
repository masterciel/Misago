from ... import threads
from ..base import BaseCommand


class Command(BaseCommand):
    help = "Moves threads and posts from Misago 0.5"

    def handle(self, *args, **options):
        self.stdout.write("Moving threads from Misago 0.5:")

        self.start_timer()
        threads.move_threads(self.stdout, self.style)
        self.stdout.write(
            self.style.SUCCESS("Moved threads in %s" % self.stop_timer()))

        self.start_timer()
        threads.move_posts()
        self.stdout.write(
            self.style.SUCCESS("Moved posts in %s" % self.stop_timer()))

        self.start_timer()
        threads.move_mentions()
        self.stdout.write(
            self.style.SUCCESS("Moved mentions in %s" % self.stop_timer()))

        self.start_timer()
        threads.move_edits()
        self.stdout.write(
            self.style.SUCCESS("Moved edits histories in %s" % self.stop_timer()))

        self.start_timer()
        threads.move_likes()
        self.stdout.write(
            self.style.SUCCESS("Moved likes in %s" % self.stop_timer()))

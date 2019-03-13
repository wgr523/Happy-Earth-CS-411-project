from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'TMP'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        #for poll_id in options['poll_id']:
        self.stdout.write("TMP try")

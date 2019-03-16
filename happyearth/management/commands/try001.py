from django.core.management.base import BaseCommand, CommandError

from happyearth.models import *

class Command(BaseCommand):
    help = 'TMP'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        #for poll_id in options['poll_id']:
        self.stdout.write("try this function.")
        newdish = Dish(name="gooddish", flavor="chinese", description="anything")
        newdish.save()

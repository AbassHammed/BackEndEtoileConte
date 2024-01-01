from django.core.management.base import BaseCommand

from etoileconte.views import get_audio 

class Command(BaseCommand):
    help = 'Populate the database with new stories and audio files'

    def handle(self, *args, **kwargs):
        # Call the function
        get_audio()
        self.stdout.write(self.style.SUCCESS('Successfully populated database with new story'))

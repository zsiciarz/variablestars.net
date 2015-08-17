from optparse import make_option

from django.core.management.base import BaseCommand

from pyaavso.utils import download_observations

from observations.utils import dict_to_observation
from observers.models import Observer


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--observer',
            action='store',
            dest='observer',
            help='AAVSO observer code'
        ),
    )

    def handle(self, *args, **options):
        observer = Observer.objects.get(aavso_code=options['observer'])
        observations = download_observations(options['observer'])
        for observation in observations:
            try:
                observation = dict_to_observation(observation, observer)
                observation.save()
            except Exception as e:
                print(e)
                continue
        self.stdout.write('Imported %d observations.' % len(observations))

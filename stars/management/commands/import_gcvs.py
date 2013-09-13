from __future__ import unicode_literals

from optparse import make_option

from django.core.management.base import BaseCommand

from pygcvs import read_gcvs

from stars.models import Star


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--file',
            action='store',
            dest='file',
            help='Path to GCVS data file'
        ),
    )

    def handle(self, *args, **options):
        new_stars = 0
        for star_dict in read_gcvs(options['file']):
            try:
                star = Star.objects.get(name=star_dict['name'])
            except Star.DoesNotExist:
                star = Star.objects.create(**star_dict)
                new_stars += 1
        self.stdout.write('Imported %d new stars.' % new_stars)
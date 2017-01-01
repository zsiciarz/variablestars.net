from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Observer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('aavso_code', models.CharField(default='', help_text='This is the code that is officially assigned to you by AAVSO.', max_length=10, verbose_name='AAVSO observer code', blank=True)),
                ('limiting_magnitude', models.FloatField(default=6.0, help_text='The magnitude of the faintest stars you can see with your eyes/binoculars/telescope. Setting this value will affect which stars will have their brightness value(s) grayed out.', null=True, verbose_name='Limiting magnitude of your equipment', blank=True)),
                ('location', geoposition.fields.GeopositionField(max_length=42, blank=True)),
                ('user', models.OneToOneField(related_name='observer', editable=False, to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
                'ordering': ('-created',),
                'verbose_name': 'Observer',
                'verbose_name_plural': 'Observers',
            },
            bases=(models.Model,),
        ),
    ]

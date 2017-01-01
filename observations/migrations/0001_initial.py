from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stars', '0001_initial'),
        ('observers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jd', models.FloatField(verbose_name='Julian Date')),
                ('magnitude', models.FloatField(verbose_name='Brightness')),
                ('fainter_than', models.BooleanField(default=False, verbose_name='Fainter than given magnitude')),
                ('comp1', models.CharField(default='', max_length=5, verbose_name='First comparison star', blank=True)),
                ('comp2', models.CharField(default='', max_length=5, verbose_name='Second comparison star', blank=True)),
                ('comment_code', models.CharField(default='', max_length=10, verbose_name='Comment code', blank=True)),
                ('chart', models.CharField(default='', max_length=20, verbose_name='Chart', blank=True)),
                ('notes', models.CharField(default='', max_length=100, verbose_name='Additional notes', blank=True)),
                ('observer', models.ForeignKey(related_name='observations', verbose_name='Observer', to='observers.Observer', on_delete=models.CASCADE)),
                ('star', models.ForeignKey(related_name='observations', verbose_name='Star', to='stars.Star', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name': 'Observation',
                'verbose_name_plural': 'Observations',
            },
            bases=(models.Model,),
        ),
    ]

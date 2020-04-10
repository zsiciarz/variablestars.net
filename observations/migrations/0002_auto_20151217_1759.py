# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("observations", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="observation",
            options={
                "verbose_name": "Observation",
                "ordering": ["-jd"],
                "verbose_name_plural": "Observations",
            },
        ),
    ]

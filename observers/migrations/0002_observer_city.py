# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ("observers", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="observer",
            name="city",
            field=models.CharField(max_length=255, blank=True, default=""),
        ),
    ]

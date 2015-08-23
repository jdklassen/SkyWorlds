# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universe', '0005_auto_20150823_0632'),
    ]

    operations = [
        migrations.AddField(
            model_name='planet',
            name='last_charred',
            field=models.DateTimeField(null=True),
        ),
    ]

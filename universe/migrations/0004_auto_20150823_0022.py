# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universe', '0003_auto_20150822_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ship',
            name='maintainence_tech',
            field=models.IntegerField(default=0),
        ),
    ]

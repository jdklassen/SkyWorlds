# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universe', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ship',
            name='research',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ship',
            name='structure_tech',
            field=models.IntegerField(default=8),
        ),
        migrations.AlterField(
            model_name='ship',
            name='tutorial_step',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ship',
            name='x',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ship',
            name='y',
            field=models.IntegerField(default=0),
        ),
    ]

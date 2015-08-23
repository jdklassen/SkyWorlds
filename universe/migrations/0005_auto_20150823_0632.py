# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universe', '0004_auto_20150823_0022'),
    ]

    operations = [
        migrations.AddField(
            model_name='ship',
            name='name',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='planet',
            name='orbit',
            field=models.IntegerField(choices=[(0, 'unbearably hot and spinning close its sun'), (1, 'warm due to its proximity to the sun'), (2, 'with a pleasant warthm from the sun'), (3, 'of a temperate climate'), (4, 'somewhat cooled by the distance to its sun'), (5, 'rather colder than preferred'), (6, 'far from its sun')]),
        ),
    ]

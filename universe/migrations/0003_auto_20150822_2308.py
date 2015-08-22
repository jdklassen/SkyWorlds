# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('universe', '0002_auto_20150822_2129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Galaxy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('galaxy', models.IntegerField(default=0, unique=True)),
                ('X_RADIUS', models.IntegerField(default=20)),
                ('Y_RADIUS', models.IntegerField(default=20)),
            ],
        ),
        migrations.AlterField(
            model_name='ship',
            name='food',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='ship',
            name='metal',
            field=models.IntegerField(default=5),
        ),
    ]

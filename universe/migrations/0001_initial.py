# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Planet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('size', models.IntegerField(choices=[(0, 'miniscule'), (1, 'tiny'), (2, 'small'), (3, 'medium'), (4, 'large'), (5, 'great'), (6, 'gigantic')])),
                ('orbit', models.IntegerField(choices=[(0, 'unbearably hot and spinning close the its sun'), (1, 'warm due to its proximity to the sun'), (2, 'with a pleasant warthm from the sun'), (3, 'of a temperate climate'), (4, 'somewhat cooled by the distance to its sun'), (5, 'rather colder than preferred'), (6, 'far from its sun')])),
                ('greenness', models.IntegerField()),
                ('minerals', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Ship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('tutorial_step', models.IntegerField()),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('population', models.IntegerField(default=1)),
                ('living_space', models.IntegerField(default=10)),
                ('restlessness', models.IntegerField(default=0)),
                ('happiness', models.IntegerField(default=50)),
                ('farms', models.IntegerField(default=1)),
                ('food', models.IntegerField(default=0)),
                ('freezer_space', models.IntegerField(default=10)),
                ('miners', models.IntegerField(default=1)),
                ('metal', models.IntegerField(default=0)),
                ('cargo_space', models.IntegerField(default=10)),
                ('research', models.IntegerField()),
                ('structure_tech', models.IntegerField(default=40)),
                ('maintainence_tech', models.IntegerField(default=1)),
                ('contentment_tech', models.IntegerField(default=0)),
                ('current_event', models.IntegerField(choices=[(0, 'Nothing'), (1, 'Alien Ruins Discovered'), (2, 'Pirate Attack'), (3, 'Hostile Aliens'), (4, 'Dangerous Nebula'), (5, 'Killer Virus')], default=0)),
                ('has_sub_surface_scanner', models.BooleanField(default=False)),
                ('has_defense_system', models.BooleanField(default=False)),
                ('has_alien_translator', models.BooleanField(default=False)),
                ('has_particle_shield', models.BooleanField(default=False)),
                ('has_omni_anti_virus', models.BooleanField(default=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='planet',
            unique_together=set([('x', 'y')]),
        ),
    ]

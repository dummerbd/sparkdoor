# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spark', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SparkCloudCredentials',
            new_name='CloudCredentials',
        ),
        migrations.RenameModel(
            old_name='SparkDevice',
            new_name='Device',
        ),
    ]

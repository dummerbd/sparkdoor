# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spark', '0003_auto_20141021_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cloudcredentials',
            name='access_token',
            field=models.CharField(max_length=250, unique=True),
        ),
    ]

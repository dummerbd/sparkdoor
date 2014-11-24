# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spark', '0005_auto_20141028_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='app_name',
            field=models.CharField(max_length=100, default='default'),
            preserve_default=True,
        ),
    ]

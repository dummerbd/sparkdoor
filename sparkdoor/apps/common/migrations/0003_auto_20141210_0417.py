# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_idcard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idcard',
            name='uid',
            field=models.CharField(max_length=10),
            preserve_default=True,
        ),
    ]

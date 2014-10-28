# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spark', '0002_auto_20141018_0202'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='name',
            field=models.CharField(default='none', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterUniqueTogether(
            name='device',
            unique_together=set([('name', 'user')]),
        ),
    ]

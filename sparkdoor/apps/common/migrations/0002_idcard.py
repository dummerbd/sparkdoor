# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spark', '0006_device_app_name'),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IDCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('uid', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('device', models.ForeignKey(to='spark.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

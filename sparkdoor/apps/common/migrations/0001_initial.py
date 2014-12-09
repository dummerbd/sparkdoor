# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spark', '0006_device_app_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoorEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('time', models.DateTimeField(auto_now=True)),
                ('event', models.CharField(max_length=50, choices=[(('open',), 'open'), ('use_pass', 'use pass')])),
                ('event_data', models.TextField(blank=True)),
                ('device', models.ForeignKey(to='spark.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DoorPass',
            fields=[
                ('token', models.CharField(max_length=40, serialize=False, primary_key=True)),
                ('expires_at', models.DateTimeField(null=True)),
                ('use_limit', models.IntegerField(null=True)),
                ('uses', models.IntegerField(default=0)),
                ('device', models.ForeignKey(to='spark.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

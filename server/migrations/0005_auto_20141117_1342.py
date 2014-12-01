# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0004_auto_20141117_1306'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='activation_key',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='key_expires',
        ),
    ]

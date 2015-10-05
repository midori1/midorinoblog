# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0012_auto_20151003_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='outline',
            field=models.TextField(default='nothing'),
            preserve_default=False,
        ),
    ]

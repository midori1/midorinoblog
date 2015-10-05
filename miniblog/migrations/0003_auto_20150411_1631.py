# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('miniblog', '0002_auto_20150410_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='classification',
            field=models.ForeignKey(to='miniblog.Classification', blank=True),
            preserve_default=True,
        ),
    ]
